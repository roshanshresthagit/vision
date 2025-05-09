import { useState } from "react";
import "./sidebar.css";

const SidebarItem = ({ item, onDragStart, searchTerm }) => {
  const [isCollapsed, setIsCollapsed] = useState(true);

  const matchesSearch = (text) =>
    text.toLowerCase().includes(searchTerm.toLowerCase());

  const filteredChildren = item.children
    ? Object.entries(item.children).filter(([key]) => matchesSearch(key))
    : [];

  const filteredMethods = item.methods
    ? Object.entries(item.methods).filter(([_, method]) => matchesSearch(method.label))
    : [];

  // If nothing matches search, skip rendering
  if (
    searchTerm &&
    filteredChildren.length === 0 &&
    filteredMethods.length === 0 &&
    !matchesSearch(item.label)
  ) {
    return null;
  }

  return (
    <div className="sidebar-item">
      <button
        className="function-button"
        onClick={() => setIsCollapsed(!isCollapsed)}
      >
        {item.children || item.methods ? (isCollapsed ? "▶" : "▼") : null} {item.label}
      </button>

      {!isCollapsed && filteredChildren.length > 0 && (
        <div className="sidebar-children">
          {filteredChildren.map(([key, child]) => (
            <SidebarItem
              key={key}
              item={{ label: key, ...child }}
              onDragStart={onDragStart}
              searchTerm={searchTerm}
            />
          ))}
        </div>
      )}

      {!isCollapsed && filteredMethods.length > 0 && (
        <div className="sidebar-methods">
          {filteredMethods.map(([key, method]) => (
            <button
              key={key}
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
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div className="sidebar-container">
      {isVisible && (
        <div className="sidebar">
          {/* Search Bar */}
          <input
            type="text"
            placeholder="Search functions..."
            className="sidebar-search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />

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
            className="function-button"
            draggable
            onDragStart={(event) =>
              onDragStart(event, { id: "modelinput", label: "Model Input", func: "modelinput" })
            }
          >
            Model Input
          </button>
          <button
            className="function-button"
            draggable
            onDragStart={(event) =>
              onDragStart(event, { id: "modelnode", label: "Model Node", func: "modelnode" })
            }
          >
            Model Node
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

          {/* Function List */}
          <div className="function-list">
            {Object.entries(functionListCall).map(([key, item]) => (
              <SidebarItem
                key={key}
                item={{ label: key, ...item }}
                onDragStart={onDragStart}
                searchTerm={searchTerm}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;
