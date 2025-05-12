### Adding a New Constant Node to the Project

To add a new constant node to the project, follow these steps:

1. **Create the Node in the `Nodes` Folder**:
    - Navigate to the `Nodes` folder.
    - Add the new node by creating a file or modifying an existing one.
    - Implement all required functionality, including its design and behavior.

2. **Update the `nodes.js` File in Constants**:
    - Open the `nodes.js` file located in the `constants` directory.
    - Add the new node to the list of DefaulInputList and nodeTypes.

3. **Modify the `useNodeDrop` Hook**:
    - Locate the `useNodeDrop` hook in the project.
    - Update the hook to handle the new node appropriately.

4. **Update the Sidebar for Display**:
    - Navigate to the `sidebar.jsx` file in the `components` directory.
    - Modify the file to include the new node so it can be displayed on the page.

By following these steps, you can successfully add a new constant node to the project.
when adding a new node that dosen't come from the backend first add node in Nodes folder write all functionality its design and whatever and then add it to nodes.js in constants and then change in useNodeDrop hooks and lastly to display it in page change is sidebar.jsx which is in components 