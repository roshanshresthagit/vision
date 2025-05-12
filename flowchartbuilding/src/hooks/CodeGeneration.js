export const useCodeGeneration = (nodes, edges, functionDefinitions) => {
  const generatePythonCode = () => {
    console.log("Generating Python code...", functionDefinitions);
    let code = "# Auto-generated Python script\n\n";

    // 1. Find all used functions
    const functionNodes = nodes.filter(node => node.type === "functionNode");
    const usedFunctions = new Set(functionNodes.map(node => node.data.func));

    // 2. Extract only the needed function definitions with original parameters
    const allDefinitions = {};
    if (functionDefinitions) {
      for (const category in functionDefinitions) {
        if (typeof functionDefinitions[category] === 'object') {
          Object.assign(allDefinitions, functionDefinitions[category]);
        }
      }
    }
    const extractedFunctions = {};
    
    Object.entries(allDefinitions).forEach(([className, classCode]) => {
      // Find all method definitions in the class
      const methodDefinitions = classCode.match(/def\s+(\w+)\(([^)]*)\):[^]+?(?=\n\s*(def|class|$))/g) || [];
      
      methodDefinitions.forEach(methodDef => {
        const funcNameMatch = methodDef.match(/def\s+(\w+)\(/);
        if (funcNameMatch && usedFunctions.has(funcNameMatch[1])) {
          // Extract the original parameters
          const paramsMatch = methodDef.match(/def\s+\w+\(([^)]*)\)/);
          const originalParams = paramsMatch ? paramsMatch[1].replace(/\s*self\s*,?\s*/, '') : '';
          
          // Store the function with its original parameters
          extractedFunctions[funcNameMatch[1]] = {
            code: methodDef
              .replace(/\bself\./g, '') // Remove self references
              .replace(/\(\s*self\s*,?\s*/, '(') // Remove self parameter
              .replace(/,\s*\)/, ')'), // Clean up trailing commas
            params: originalParams
          };
        }
      });
    });

    // Add the extracted functions to code
    Object.values(extractedFunctions).forEach(func => {
      code += `${func.code}\n\n`;
    });

    // 3. Add input values
    const inputs = nodes.filter(node => node.type === "inputNode"|| node.type === "imageInputNode");
    inputs.forEach(input => {
      if (input.data?.func && input.data?.value !== undefined) {
        code += `${input.data.func} = ${input.data.value}\n`;
      }
    });

    // 4. Generate function calls with correct parameter mapping
    const functionCalls = {};
    edges.forEach(({ source, target }) => {
      if (!functionCalls[target]) functionCalls[target] = [];
      functionCalls[target].push(source);
    });

    Object.entries(functionCalls).forEach(([target, sources]) => {
      const targetNode = nodes.find(n => n.id === target);
      if (targetNode?.type === "functionNode" && targetNode.data?.func) {
        const funcName = targetNode.data.func;
        const funcInfo = extractedFunctions[funcName];
        
        // Create mapping between parameter names and source values
        const paramNames = funcInfo?.params.split(',').map(p => p.trim()).filter(p => p) || [];
        const sourceValues = sources.map((sourceId, i) => {
          const sourceNode = nodes.find(n => n.id === sourceId);
          return sourceNode?.type === "inputNode" || sourceNode?.type === "imageInputNode" 
            ? sourceNode.data?.func 
            : `${targetNode.data.func.toLowerCase()}${sourceId}`;
        }).filter(Boolean);
        
        // Pair parameters with values (or use defaults if not enough sources)
        const paramsWithValues = paramNames.map((param, i) => 
          sourceValues[i] !== undefined ? sourceValues[i] : param
        ).join(', ');

        code += `${funcName.toLowerCase()}${targetNode.id} = ${funcName}(${paramsWithValues})\n`;
      }
    });

    // 5. Add final output
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