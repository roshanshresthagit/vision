export const useCodeGeneration = (nodes, edges, functionDefinitions) => {
  const generatePythonCode = () => {
    let code = "# Auto-generated Python script\n\n";

    // 1. Find all used functions
    const functionNodes = nodes.filter(node => node.type === "functionNode");
    const usedFunctions = new Set(functionNodes.map(node => node.data.func));

    // 2. Extract relevant function definitions
    const extractedFunctions = {};

    if (functionDefinitions && typeof functionDefinitions === 'object') {
      for (const fullFuncKey in functionDefinitions) {
        const funcCode = functionDefinitions[fullFuncKey];
        const shortFuncNameMatch = fullFuncKey.match(/\.([^.]+)$/);
        const shortFuncName = shortFuncNameMatch?.[1];

        if (shortFuncName && usedFunctions.has(shortFuncName) && funcCode) {
          const processedCode = funcCode
            .replace(/def\s+(\w+)\(/, `def ${shortFuncName}(`)         
            .replace(/(def\s+\w+\()\s*self,?\s*/, '$1');              

          extractedFunctions[shortFuncName] = processedCode;
        }
      }
    }

    // 3. Add function definitions to the code
    Object.keys(extractedFunctions).sort().forEach(fn => {
      code += `${extractedFunctions[fn]}\n\n`;
    });

    // 4. Add input values
    const inputs = nodes.filter(node => node.type === "inputNode" || node.type === "imageInputNode");
    inputs.forEach(input => {
      if (input.data?.func && input.data?.value !== undefined) {
        code += `${input.data.func+ input.id} = ${input.data.value}\n`;
      }
    });

    code += "\n";

    // 5. Generate function calls
    const functionCalls = {};
    edges.forEach(({ source, target }) => {
      if (!functionCalls[target]) functionCalls[target] = [];
      functionCalls[target].push(source);
    });

    Object.entries(functionCalls).forEach(([target, sources]) => {
      const targetNode = nodes.find(n => n.id === target);
      if (targetNode?.type === "functionNode" && targetNode.data?.func) {
        const funcName = targetNode.data.func;
        const funcCode = extractedFunctions[funcName];

        const paramNamesMatch = funcCode ? funcCode.match(/\(([^)]*)\)/) : null;
        const paramNames = paramNamesMatch 
          ? paramNamesMatch[1].split(',').map(p => p.trim()).filter(p => p) 
          : [];

        const sourceValues = sources.map((sourceId) => {
          const sourceNode = nodes.find(n => n.id === sourceId);
          if (!sourceNode) return null;

          if (sourceNode.type === "inputNode" || sourceNode.type === "imageInputNode") {
            return `${sourceNode.data?.func}${sourceNode.id}`;
          } else if (sourceNode.type === "functionNode") {
            return `${sourceNode.data?.func?.toLowerCase()}${sourceNode.id}`;
          }
          return null;
        }).filter(Boolean);

        const paramsWithValues = paramNames
          .map((param, i) => sourceValues[i] || param)
          .join(', ');

        code += `${funcName.toLowerCase()}${targetNode.id} = ${funcName}(${paramsWithValues})\n`;
      }
    });

    // 6. Add final output print(s)
    const resultNodes = nodes.filter(node => node.type === "resultNode");
    resultNodes.forEach(resultNode => {
      const lastEdge = edges.find(edge => edge.target === resultNode.id);
      if (lastEdge) {
        const lastFunction = nodes.find(node => node.id === lastEdge.source);
        if (lastFunction?.data?.func) {
          code += `print("Final Result:", ${lastFunction.data.func.toLowerCase()}${lastFunction.id})\n`;
        }
      }
    });

    return code;
  };

  return { generatePythonCode };
};
