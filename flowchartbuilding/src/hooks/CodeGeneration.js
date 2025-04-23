export const useCodeGeneration = (nodes, edges, functionDefinitions) => {
  const generatePythonCode = () => {
    let code = "# Auto-generated Python script\n\n";

    // 1. Extract and include only the methods used
    const functionNodes = nodes.filter((node) => node.type === "functionNode");
    const extractedMethods = new Set();

    functionNodes.forEach((node) => {
      const methodName = node.data.func;

      for (const classCode of Object.values(functionDefinitions)) {
        const regex = new RegExp(
          `\\s*def ${methodName}\\([^\\)]*\\):[\\s\\S]*?(?=\\n\\s*def |\\n\\s*class |$)`,
          "g"
        );
        const matches = classCode.match(regex);
        if (matches && matches.length > 0 && !extractedMethods.has(methodName)) {
          let functionCode = matches[0].trimStart();

          functionCode = functionCode.replace(/\((\s*self\s*,?|\s*self\s*)\)/, "()");

          functionCode = functionCode.replace(/\(\s*self\s*,\s*/, "(");

          code += functionCode + "\n\n";
          extractedMethods.add(methodName);
        }
      }
    });

    // 2. Define input values
    const inputs = nodes.filter((node) => node.type === "inputNode");
    inputs.forEach((input) => {
      code += `${input.data.func + input.id} = ${input.data.value}\n`;
    });

    // 3. Map function calls based on edges
    const functionCalls = {};
    edges.forEach(({ source, target }) => {
      if (!functionCalls[target]) {
        functionCalls[target] = [];
      }
      functionCalls[target].push(source);
    });

    // 4. Generate function calls
    Object.keys(functionCalls).forEach((target) => {
      const targetNode = nodes.find((n) => n.id === target);
      if (targetNode && targetNode.type === "functionNode") {
        const sources = functionCalls[target]
          .map((id) => nodes.find((n) => n.id === id).data.func + id)
          .join(", ");
        code += `${targetNode.data.label + targetNode.id} = ${targetNode.data.func}(${sources})\n`;
      }
    });

    // 5. Capture final result
    const resultNode = nodes.find((node) => node.type === "resultNode");
    if (resultNode) {
      const lastEdge = edges.find((edge) => edge.target === resultNode.id);
      const lastFunction = nodes.find((node) => node.id === lastEdge?.source);
      if (lastFunction) {
        code += `print("Final Result:", ${lastFunction.data.label + lastFunction.id})\n`;
      }
    }

    return code;
  };

  return { generatePythonCode };
};
