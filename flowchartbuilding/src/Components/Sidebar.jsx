import React, { useState, useEffect } from "react";
import "./sidebar.css";

const Sidebar = ({ onDragStart, functionListCall, isVisible }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Debugging to check if functionListCall has data
  useEffect(() => {
    console.log("Function List Call:", functionListCall);
  }, [functionListCall]);

  const filteredFunctions = functionListCall.filter((func) =>
    func.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Debugging to see filtered results
  useEffect(() => {
    console.log("Filtered Functions:", filteredFunctions);
  }, [filteredFunctions]);

  return (
    <div className="sidebar-container">
      {isVisible && (
        <div className="sidebar">
          {/* Search Bar */}
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

          {/* Collapsible Functions Section */}
          <button className="collapse-button function-button" onClick={() => setIsCollapsed(!isCollapsed)}>
            {isCollapsed ? "Show Functions ▼" : "Hide Functions ▲"}
          </button>

          {!isCollapsed && (
            <div className="function-list">
              {filteredFunctions.length > 0 ? (
                filteredFunctions.map((func) => (
                  <button
                    key={func.id}
                    className="function-button"
                    draggable
                    onDragStart={(event) => onDragStart(event, func)}
                  >
                    {func.label}
                  </button>
                ))
              ) : (
                <p className="no-functions">No functions found</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Sidebar;
