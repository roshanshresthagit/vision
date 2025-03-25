import React, { useState } from "react";
import './sidebar.css'
const Sidebar = ({ onDragStart, functionListCall, isVisible }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredFunctions = functionListCall.filter((func) =>
    func.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="sidebar-container">
      {isVisible && (
        <div className="sidebar">
          <div className="search-bar-container">
            <i className="fa fa-search search-icon"></i>
            <input
              type="text"
              placeholder="Search functions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-bar"
            />
          </div>
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
          onDragStart={(event)=>
            onDragStart(event,{id:"imageinput", label:"ImageInput", func:"imageinput"})
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
          {filteredFunctions.map((func) => (
            <button
              key={func.id}
              className="function-button"
              draggable
              onDragStart={(event) => onDragStart(event, func)}
            >
              {func.label}
            </button>
          ))}
          
        </div>
      )}
    </div>
  );
};

export default Sidebar;
