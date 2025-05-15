export const useCodeGeneration = (nodes, edges, functionDefinitions) => {
  const generatePythonCode = () => {
    let code = "# Auto-generated Python script\n\n";
    code += "import cv2\n";
    code += "import numpy as np\n";
    
     
    // Handle image input separately (passed as argument to main)
    const input = nodes.find(node => node.type === "imageInputNode");
    if (input) {
      code += "\ndef main(imageinput1):\n";
    }
    else {
      code += "\ndef main():\n";
    }
    
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

        // Handle different source types
        if (sourceNode.type === "imageInputNode") {
          return `${paramName}=imageinput1`;  // Use the main function argument
        } else if (sourceNode.type === "inputNode") {
          return `${paramName}=${sourceNode.data?.value}`;  // Use value directly
        } else {
          // For function nodes, use their generated variable name
          return `${paramName}=${sourceNode.data?.func?.toLowerCase()}${sourceNode.id}`;
        }
      }).filter(Boolean);

      code += `\t${funcName.toLowerCase()}${node.id} = ${funcName}(${args.join(', ')})\n`;
    });

    // Handle result nodes
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