export const useCodeGeneration = (nodes, edges, functionDefinitions) => {
  const generatePythonCode = () => {
    let code = "# Auto-generated Python script\n\n";
    console.log("nodes", nodes);
     
    // Input nodes generation remains the same
    const inputs = nodes.filter(node => node.type === "inputNode" || node.type === "imageInputNode");
    inputs.forEach(input => {
      if (input.data?.func && input.data?.value !== undefined) {
        code += `${input.data.func}${input.id} = ${input.data.value}\n`;
      }
    });
    
    code += "\ndef main():\n";

    // Function extraction remains the same
    const functionNodes = nodes.filter(node => node.type === "functionNode");
    const usedFunctions = new Set(functionNodes.map(node => node.data.func));
    const extractedFunctions = {};

    if (functionDefinitions) {
      for (const fullFuncKey in functionDefinitions) {
        const funcCode = functionDefinitions[fullFuncKey];
        const shortFuncName = fullFuncKey.split('.').pop();
        if (shortFuncName && usedFunctions.has(shortFuncName) && funcCode) {
          extractedFunctions[shortFuncName] = funcCode
            .replace(/def\s+(\w+)\(/, `def ${shortFuncName}(`)
            .replace(/(def\s+\w+\()\s*self,?\s*/, '$1');
        }
      }
    }

    Object.keys(extractedFunctions).sort().forEach(fn => {
      code += `\n${extractedFunctions[fn]}\n`;
    });

    // Build connections map
    const connections = {};
    edges.forEach(edge => {
      if (!connections[edge.target]) connections[edge.target] = {};
      connections[edge.target][edge.targetHandle] = edge.source;
    });

    // Generate function calls with keyword arguments
    nodes.filter(n => n.type === "functionNode").forEach(node => {
      const funcName = node.data?.func;
      const funcCode = extractedFunctions[funcName];
      if (!funcName || !funcCode) return;

      // Get parameter names from function definition
      const paramNames = funcCode.match(/\(([^)]*)\)/)?.[1]
        ?.split(',')
        ?.map(p => p.trim().split('=')[0]) || [];

      // Generate keyword arguments
      const args = paramNames.map(paramName => {
        const sourceId = connections[node.id]?.[paramName];
        if (!sourceId) return null;

        const sourceNode = nodes.find(n => n.id === sourceId);
        if (!sourceNode) return null;

        const valuePrefix = sourceNode.type === "inputNode" || sourceNode.type === "imageInputNode"
          ? sourceNode.data?.func
          : sourceNode.data?.func?.toLowerCase();

        return `${paramName}=${valuePrefix}${sourceNode.id}`;
      }).filter(Boolean);

      code += `\t${funcName.toLowerCase()}${node.id} = ${funcName}(${args.join(', ')})\n`;
    });

    // Handle result nodes (remains the same)
    const resultNodes = nodes.filter(n => n.type === "resultNode");
    resultNodes.forEach(resultNode => {
      const lastEdge = edges.find(e => e.target === resultNode.id);
      if (lastEdge) {
        const lastFunc = nodes.find(n => n.id === lastEdge.source);
        if (lastFunc?.data?.func) {
          code += `\treturn ${lastFunc.data.func.toLowerCase()}${lastFunc.id}\n`;
        }
      }
    });

    return code;
  };

  return { generatePythonCode };
};