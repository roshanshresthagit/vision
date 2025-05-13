import "./App.css";
import TopBar from "./Components/TopBar";
import Sidebar from "./Components/Sidebar";
import FlowCanvas from "./Components/FlowCanvas";
import { useFlowData } from "./hooks/useFlowData";
import { useState } from "react";
import { useEdgeManagement } from "./hooks/useEdgeManagement";
import { nodeTypes, DefaultInputList } from "./constants/nodes";
import { useNodesState, useEdgesState, useReactFlow } from "reactflow";
import { useFlowExecution } from "./hooks/useFlowExecution";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { coy } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useFlowStorage } from "./hooks/useFlowStorage";
import { useNodeDrop } from "./hooks/useNodeDrop";
import { useNodeDeletion } from "./hooks/useNodeDeletion";

export default function App() {
  const {setViewport} = useReactFlow();
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
  const { onConnect,onEdgeUpdateStart,onEdgeUpdate,onEdgeUpdateEnd } = useEdgeManagement(setEdges);
  const { executeFlow, generatedCode, setGeneratedCode} = useFlowExecution(nodes, edges, inputs, setNodes);
  const { onDrop } = useNodeDrop({ nodeId, inputNodeCount, functionDict, setInputs, setNodes, setEdges,setNodeId, setInputNodeCount,});
  const { onDeleteNode } = useNodeDeletion({ selectedNodeId, setSelectedNodeId, setNodes, setEdges, });
  const [isCodeVisible, setIsCodeVisible] = useState(true);


  const toggleSidebar = () => {
    setIsSidebarVisible((prev) => !prev);
  };

  const onDragStart = (event, func) => {
    event.dataTransfer.setData("application/reactflow", JSON.stringify(func));
    event.dataTransfer.effectAllowed = "move";
  }
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
          {/* <SyntaxHighlighter language="python" style={coy}>
            {typeof generatedCode === "string"
              ? generatedCode
              : JSON.stringify(generatedCode, null, 2)}
          </SyntaxHighlighter> */}
          {isCodeVisible && (
            <div
              style={{
                maxWidth: "640px",
                maxHeight: "400px",
                overflow: "auto",
                border: "1px solid #ccc",
                borderRadius: "8px",
                marginTop: "16px",
                position: "relative",
                backgroundColor: "#f9f9f9",
              }}
            >
              <button
                onClick={() => setIsCodeVisible(false)}
                style={{
                  position: "absolute",
                  top: "40px",
                  right: "4px",
                  background: "#e74c3c",
                  border: "none",
                  color: "#fff",
                  padding: "4px 8px",
                  borderRadius: "4px",
                  cursor: "pointer",
                  fontSize: "12px"
                }}
              >
                Close
              </button>
              <SyntaxHighlighter
                language="python"
                style={coy}
                customStyle={{ margin: 0, padding: "1em", overflowX: "auto" }}
              >
                {typeof generatedCode === "string"
                  ? generatedCode
                  : JSON.stringify(generatedCode, null, 2)}
              </SyntaxHighlighter>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
