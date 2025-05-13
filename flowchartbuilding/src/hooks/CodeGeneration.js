export const useCodeGeneration = (nodes, edges, functionDefinitions) => {
  const generatePythonCode = () => {
    console.log("Generating Python code...", functionDefinitions);
    let code = "# Auto-generated Python script\n\n";

    // 1. Find all used functions
    const functionNodes = nodes.filter(node => node.type === "functionNode");
    const usedFunctions = new Set(functionNodes.map(node => node.data.func));

    // 2. Extract relevant function definitions (without class and 'self' parameter)
    const allDefinitions = {};
    if (functionDefinitions) {
      for (const category in functionDefinitions) {
        if (typeof functionDefinitions[category] === 'object') {
          Object.assign(allDefinitions, functionDefinitions[category]);
        }
      }
    }

    const extractedFunctions = {};

    Object.entries(allDefinitions).forEach(([fullFuncName, funcCode]) => {
      const funcNameMatch = fullFuncName.match(/\.([^\.]+)$/);
      if (funcNameMatch && funcNameMatch[1] && usedFunctions.has(funcNameMatch[1])) {
        if (funcCode) {
          // Process the function code to remove 'self' and adjust function name
          let processedCode = funcCode
            .replace(/def\s+(\w+)\(/, `def ${funcNameMatch[1]}(`)  // Ensure correct function name
            .replace(/(def\s+\w+\()\s*self,?\s*/, '$1'); // Remove 'self' parameter

          extractedFunctions[funcNameMatch[1]] = processedCode;
        }
      }
    });

    // 3. Add function definitions to the code
    Object.values(extractedFunctions).forEach(funcCode => {
      code += `${funcCode}\n\n`;
    });

    // 4. Add input values
    const inputs = nodes.filter(node => node.type === "inputNode" || node.type === "imageInputNode");
    inputs.forEach(input => {
      if (input.data?.func && input.data?.value !== undefined) {
        code += `${input.data.func} = ${input.data.value}\n`;
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

        // Extract parameter names from the processed function code
        const paramNamesMatch = funcCode ? funcCode.match(/\(([^)]*)\)/) : null;
        const paramNames = paramNamesMatch 
          ? paramNamesMatch[1].split(',').map(p => p.trim()).filter(p => p) 
          : [];

        const sourceValues = sources.map((sourceId) => {
          const sourceNode = nodes.find(n => n.id === sourceId);
          return sourceNode?.type === "inputNode" || sourceNode?.type === "imageInputNode"
            ? sourceNode.data?.func
            : `${sourceNode?.data?.func?.toLowerCase() || 'val'}${sourceNode?.id}`;
        }).filter(Boolean);

        // Ensure we have enough parameters or use the available sources
        const paramsWithValues = paramNames
          .map((param, i) => sourceValues[i] || param)
          .join(', ');

        code += `${funcName.toLowerCase()}${targetNode.id} = ${funcName}(${paramsWithValues})\n`;
      }
    });

    // 6. Add final output
    const resultNode = nodes.find(node => node.type === "resultNode");
    if (resultNode) {
      const lastEdge = edges.find(edge => edge.target === resultNode.id);
      if (lastEdge) {
        const lastFunction = nodes.find(node => node.id === lastEdge.source);
        if (lastFunction) {
          code += `print("Final Result:", ${lastFunction.data.func.toLowerCase()}${lastFunction.id})\n`;
        }
      }
    }

    return code;
  };

  return { generatePythonCode };
};