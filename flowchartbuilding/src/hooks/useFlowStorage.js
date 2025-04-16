import { useCallback } from 'react';

const flowKey = 'example-flow';

export const useFlowStorage = ({ rfInstance, setNodes, setEdges, setViewport }) => {
  const onSave = useCallback(() => {
    if (rfInstance) {
      const flow = rfInstance.toObject();
      localStorage.setItem(flowKey, JSON.stringify(flow));
    console.log('Flow saved!');
    }
  }, [rfInstance]);

  const onRestore = useCallback(() => {
    const restore = async () => {
      const flow = JSON.parse(localStorage.getItem(flowKey));
      if (flow) {
        const { x = 0, y = 0, zoom = 1 } = flow.viewport;
        setNodes(flow.nodes || []);
        setEdges(flow.edges || []);
        setViewport({ x, y, zoom });
        console.log('Flow restored!');
      }
    };
    restore();
  }, [setNodes, setEdges, setViewport]);

  return { onSave, onRestore };
};
