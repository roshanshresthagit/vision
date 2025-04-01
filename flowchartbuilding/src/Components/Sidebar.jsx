import React, { useState } from "react";
import "./sidebar.css";

const SidebarItem = ({ item, onDragStart }) => {
  const [isCollapsed, setIsCollapsed] = useState(true);

  return (
    <div className="sidebar-item">
      <button
        className="function-button"
        onClick={() => setIsCollapsed(!isCollapsed)}
      >
        {item.children || item.methods ? (isCollapsed ? "▶" : "▼") : null} {item.label}
      </button>
      
      {!isCollapsed && item.children && (
        <div className="sidebar-children">
          {Object.entries(item.children).map(([key, child]) => (
            <SidebarItem key={key} item={{ label: key, ...child }} onDragStart={onDragStart} />
          ))}
        </div>
      )}
      
      {!isCollapsed && item.methods && (
        <div className="sidebar-methods">
          {item.methods.map((method) => (
            <button
              key={method.id}
              className="function-button"
              draggable
              onDragStart={(event) => onDragStart(event, method)}
            >
              {method.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

const Sidebar = ({ onDragStart, functionListCall, isVisible }) => {
  return (
    <div className="sidebar-container">
      {isVisible && (
        <div className="sidebar">
          {/* Static Buttons */}
          <button
            className="function-button"
            draggable
            onDragStart={(event) =>
              onDragStart(event, { id: "input", label: "Input", func: "input" })
            }
          >
            Input
          </button>
          <button
            className="function-button"
            draggable
            onDragStart={(event) =>
              onDragStart(event, { id: "imageinput", label: "Image Input", func: "imageinput" })
            }
          >
            Image Input
          </button>
          <button
            className="function-button result-button"
            draggable
            onDragStart={(event) =>
              onDragStart(event, { id: "result", label: "Result", func: "result" })
            }
          >
            Result
          </button>
          
          {/* Recursive Sidebar Items */}
          <div className="function-list">
            {Object.entries(functionListCall).map(([key, item]) => (
              <SidebarItem key={key} item={{ label: key, ...item }} onDragStart={onDragStart} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;