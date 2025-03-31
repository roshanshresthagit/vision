import "./App.css";
import TopBar from "./Components/TopBar";
import Sidebar from "./Components/Sidebar";
import FlowCanvas from "./Components/FlowCanvas";
import { useFlowData } from "./hooks/useFlowData";
import React, { useState, useCallback } from "react";
import { useEdgeManagement } from "./hooks/useEdgeManagement";
import { nodeTypes, DefaultInputList } from "./constants/nodes";
import { useNodesState, useEdgesState } from "reactflow";

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [nodeId, setNodeId] = useState(1);
  const [inputs, setInputs] = useState({});
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [generatedCode, setGeneratedCode] = useState("");
  const [inputNodeCount, setInputNodeCount] = useState(DefaultInputList);
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const { functionDict, functionList, functionDefinitions } = useFlowData();
  const { onConnect,onEdgeUpdateStart,onEdgeUpdate,onEdgeUpdateEnd } = useEdgeManagement(setEdges);


  const toggleSidebar = () => {
    setIsSidebarVisible((prev) => !prev);
  };

  const onDragStart = (event, func) => {
    event.dataTransfer.setData("application/reactflow", JSON.stringify(func));
    event.dataTransfer.effectAllowed = "move";
  };

  // Handle drop
  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const reactFlowBounds = event.target.getBoundingClientRect();
      const func = JSON.parse(event.dataTransfer.getData("application/reactflow"));
      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };
  
      const newNodeId = `${nodeId}`;
  
      const isInput = func.id === "input";
      const isImageInput = func.id === "imageinput";
  
      const newNode = {
        id: newNodeId,
        type: isInput
          ? "inputNode"
          : isImageInput
          ? "imageInputNode"
          : func.id === "result"
          ? "resultNode"
          : "functionNode",
        position,
        data: {
          label: isInput
            ? `${func.label}${inputNodeCount}`
            : isImageInput
            ? `${func.label}${inputNodeCount}`
            : func.label,
          func: func.func,
          value: isInput || isImageInput ? 0 : undefined, // Initially set to 0 for both input and imageinput
          setValue:
            isInput || isImageInput
              ? (val) =>
                  setInputs((prev) => {
                    const updatedInputs = { ...prev, [newNodeId]: val };
                    setNodes((nds) =>
                      nds.map((node) =>
                        node.id === newNodeId
                          ? { ...node, data: { ...node.data, value: val } }
                          : node
                      )
                    );
                    return updatedInputs;
                  })
              : undefined,
          functionDict,
        },
      };
  
      setNodes((nds) => [...nds, newNode]);
      setNodeId((id) => id + 1);
  
      if (isInput || isImageInput) {
        setInputNodeCount((count) => count + 1);
      }
    },
    [setNodes, nodeId, inputNodeCount, functionDict]
  );
  
  // Delete node
  const onDeleteNode = () => {
    if (selectedNodeId) {
      setNodes((nds) => nds.filter((node) => node.id !== selectedNodeId));
      setEdges((eds) => eds.filter((edge) => edge.source !== selectedNodeId && edge.target !== selectedNodeId));
      setSelectedNodeId(null);
    }
  };

  const executeFlow = async () => {
    const nodeValues = {};

    for (const node of nodes) {
      if (node.type === "inputNode"|| "imageInputNode") {
        const inputValue = inputs[node.id];
        if (typeof inputValue === "string" && inputValue.startsWith("data:image")) {
          nodeValues[node.id] = inputValue;
        } else {
          nodeValues[node.id] = parseFloat(inputValue) || 0;
        }
      }
    }

    try {
      const response = await fetch("http://localhost:8000/execute_flow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nodes,
          edges,
          inputValues: nodeValues,
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        let newlineIndex;
        while ((newlineIndex = buffer.indexOf("\n")) >= 0) {
          const line = buffer.slice(0, newlineIndex).trim();
          buffer = buffer.slice(newlineIndex + 1);

          if (line) {
            console.log("Received line:", line);

            const data = JSON.parse(line);

            if (data.resultNode) {
              console.log(`ResultNode ${data.resultNode}:`, data.value);

              nodeValues[data.resultNode] = data.value;
              setNodes((nds) =>
                nds.map((node) =>
                  node.id === data.resultNode
                    ? { ...node, data: { ...node.data, value: data.value } }
                    : node
                )
              );
            } else if (data.message) {
              console.log("Message:", data.message);
            } else if (data.error) {
              console.error("Error:", data.error);
            }
          }
        }
      }
      console.log("Flow execution completed!");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="container">
      <TopBar
        toggleSidebar={toggleSidebar}
        executeFlow={executeFlow}
        onDeleteNode={onDeleteNode}
        selectedNodeId={selectedNodeId}
        nodes={nodes}
        edges={edges}
        functionDefinitions={functionDefinitions}
        setGeneratedCode={setGeneratedCode}
      />
      <div className="main-content">
        <Sidebar
          onDragStart={onDragStart}
          functionListCall={functionList}
          isVisible={isSidebarVisible}
        />
        <div className="canvas-container">
          <FlowCanvas
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onEdgeUpdate={onEdgeUpdate} 
            onEdgeUpdateStart={onEdgeUpdateStart}
            onEdgeUpdateEnd={onEdgeUpdateEnd}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            setSelectedNodeId={setSelectedNodeId}
            onDrop={onDrop}
          />
          <pre style={{ background: "#eee", padding: "10px", marginTop: "10px" }}>
            {typeof generatedCode === "string"
              ? generatedCode
              : JSON.stringify(generatedCode, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}
