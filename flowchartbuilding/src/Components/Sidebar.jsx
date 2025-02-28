import React from "react";

const Sidebar = ({ onDragStart, executeFlow, onDeleteNode, selectedNodeId , functionListCall}) => {
  const functionList = functionListCall
  return (
    <div className="sidebar">
      <h2>Blocks</h2>
      <button
        className="function-button"
        draggable
        onDragStart={(event) => onDragStart(event, { id: "input", label: "Input", func: "input" })}
      >
        Input
      </button>
      {functionList.map((func) => (
        <button
          key={func.id}
          className="function-button"
          draggable
          onDragStart={(event) => onDragStart(event, func)}
        >
          {func.label}
        </button>
      ))}
      <button
        className="function-button result-button"
        draggable
        onDragStart={(event) => onDragStart(event, { id: "result", label: "Result", func: "result" })}
      >
        Result
      </button>
      <button className="execute-button" onClick={executeFlow}>
        Execute
      </button>
      <button
        className="delete-button"
        onClick={onDeleteNode}
        disabled={!selectedNodeId}
      >
        Delete Node
      </button>
    </div>
  );
};

export default Sidebar;
