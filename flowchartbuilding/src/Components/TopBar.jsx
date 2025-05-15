import React from "react";
import { Menu } from "lucide-react";
import "./topbar.css";
import { useCodeGeneration } from "../hooks/CodeGeneration";

const TopBar = ({ 
  executeFlow,
  toggleCodeVisibility, 
  onDeleteNode, 
  selectedNodeId, 
  nodes, 
  edges, 
  functionDefinitions, 
  setGeneratedCode, 
  toggleSidebar,
  onSave,
  onRestore,
}) => {
  const { generatePythonCode } = useCodeGeneration(nodes, edges, functionDefinitions);

  const handleGenerateCode = () => {
    const code = generatePythonCode();
    setGeneratedCode(code);
    toggleCodeVisibility();
  };

  return (
    <div className="top-bar">
      <div className="top-bar-left">
        {/* Sidebar Toggle */}
        <button className="top-bar-button menu-toggle" onClick={toggleSidebar}>
          <Menu size={24} />
        </button>
        <h1 className="app-title">Flow Based System</h1>
      </div>

      <div className="top-bar-actions">
        <button className="top-bar-button execute-button" onClick={executeFlow}>
          Execute
        </button>

        <button 
          className="top-bar-button delete-button" 
          onClick={onDeleteNode} 
          disabled={!selectedNodeId}
        >
          Delete Node
        </button>

        <button 
          className="top-bar-button codegeneration-button" 
          onClick={handleGenerateCode}
        >
          Generate Code
        </button>
        {onSave && (
          <button className="top-bar-button save-button" onClick={onSave}>
            Save
          </button>
        )}
        {onRestore && (
          <button className="top-bar-button restore-button" onClick={onRestore}>
            Restore
          </button>
        )}
      </div>
    </div>
  );
};

export default TopBar;
