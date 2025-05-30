import "./App.css";
import TopBar from "./Components/TopBar";
import Sidebar from "./Components/Sidebar";
import FlowCanvas from "./Components/FlowCanvas";
import { useFlowData } from "./hooks/useFlowData";
import { useState,useRef,useEffect } from "react";
import { useNodeDrop } from "./hooks/useNodeDrop";
import { useFlowStorage } from "./hooks/useFlowStorage"
import { useNodeDeletion } from "./hooks/useNodeDeletion";
import { useFlowExecution } from "./hooks/useFlowExecution";
import { useEdgeManagement } from "./hooks/useEdgeManagement";
import { nodeTypes, DefaultInputList } from "./constants/nodes";
import { coy } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { useNodesState, useEdgesState, useReactFlow } from "reactflow";

export default function App() {
  const { setViewport } = useReactFlow();
  const [nodeId, setNodeId] = useState(1);
  const [inputs, setInputs] = useState({});
  const [rfInstance, setRfInstance] = useState(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [inputNodeCount, setInputNodeCount] = useState(DefaultInputList);
  const { functionDict, functionList, functionDefinitions } = useFlowData();
  const { onSave, onRestore } = useFlowStorage({ rfInstance, setNodes, setEdges, setViewport });
  const { onConnect, onEdgeUpdateStart, onEdgeUpdate, onEdgeUpdateEnd } = useEdgeManagement(setEdges);
  const { executeFlow, generatedCode, setGeneratedCode } = useFlowExecution(nodes, edges, inputs, setNodes);
  const { onDrop } = useNodeDrop({ nodeId, inputNodeCount, functionDict, setInputs, setNodes, setEdges, setNodeId, setInputNodeCount });
  const { onDeleteNode } = useNodeDeletion({ selectedNodeId, setSelectedNodeId, setNodes, setEdges });
  const [isCodeVisible, setIsCodeVisible] = useState(false);
  const [animatedCodeLines, setAnimatedCodeLines] = useState([])
  const codeContainerRef = useRef(null)


  
  const toggleSidebar = () => { 
    setIsSidebarVisible((prev) => !prev);
  };

  const onDragStart = (event, func) => {
    event.dataTransfer.setData("application/reactflow", JSON.stringify(func));
    event.dataTransfer.effectAllowed = "move";
  };

  const toggleCodeVisibility = () => {
    setIsCodeVisible((prev) => !prev);
  };
  const onExportCode = () => {
    const code = generatedCode;
    const blob = new Blob([code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "generated_code.py";
    a.click();
    URL.revokeObjectURL(url);
  };
  useEffect(() => {
    if (!isCodeVisible || typeof generatedCode !== "string") return;

    const lines = generatedCode.split("\n");
    setAnimatedCodeLines([]); 

    lines.forEach((line, index) => {
      setTimeout(() => {
        setAnimatedCodeLines((prev) => [...prev, line]);
      }, index * 100); //animation time
    });
  }, [generatedCode, isCodeVisible]);

  useEffect(() => {
    if (codeContainerRef.current) {
      codeContainerRef.current.scrollTop = codeContainerRef.current.scrollHeight;
    }
  }, [animatedCodeLines]);
  return (
    <div className="container">
      <TopBar
        toggleSidebar={toggleSidebar}
        executeFlow={executeFlow}
        toggleCodeVisibility={toggleCodeVisibility}
        onDeleteNode={onDeleteNode}
        selectedNodeId={selectedNodeId}
        nodes={nodes}
        edges={edges}
        functionDefinitions={functionDefinitions}
        setGeneratedCode={setGeneratedCode}
        onSave={onSave}
        onRestore={onRestore}
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
            onInit={setRfInstance}
          />
          <div
            style={{
              Width: "640px",
              maxHeight: "100%",
              overflow: "auto",
              border: "1px solid #ccc",
              borderRadius: "8px",
              marginTop: "16px",
              position: "relative",
              backgroundColor: "#f9f9f9",
            }}
          >
            <button
              onClick={toggleCodeVisibility}
              style={{
                position: "absolute",
                top: "40px",
                right: "20px",
                background: isCodeVisible ? "#e74c3c" : "#2ecc71", 
                border: "none",
                color: "#fff",
                padding: "4px 8px",
                borderRadius: "4px",
                cursor: "pointer",
                fontSize: "12px",
                zIndex: 100,
              }}
            >
              {isCodeVisible ? "Hide Code" : "Show Code"}
            </button>

            <button
              onClick={onExportCode}
              style={{
                position: "absolute",
                top: "40px",
                left: "10px",
                background:  "#2ecc71", 
                border: "none",
                color: "#fff",
                padding: "4px 8px",
                borderRadius: "4px",
                cursor: "pointer",
                fontSize: "12px",
                zIndex: 100,
              }}
            >
              Export Code
            </button>
            {isCodeVisible && (
      <SyntaxHighlighter
        language="python"
        style={coy}
        customStyle={{ margin: 0, padding: "1em", overflowX: "auto" }}
      >
        {animatedCodeLines.join("\n")}
      </SyntaxHighlighter>
    )}
            
          </div>
        </div>
      </div>
    </div>
  );
}
