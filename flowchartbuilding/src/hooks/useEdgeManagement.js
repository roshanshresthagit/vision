import { useCallback, useRef } from 'react';
import { addEdge, reconnectEdge,MarkerType } from 'reactflow';

export const useEdgeManagement = (setEdges) => {
  const edgeReconnectSuccessful = useRef(true);

  const onConnect = useCallback(
    (params) => setEdges(els => addEdge({
      ...params,
      animated: true,
      style: { stroke: 'green' },
      type: "straight",
      markerEnd: { type: MarkerType.ArrowClosed, color: 'green' }
    }, els)),
    [setEdges]
  );

  const onEdgeUpdateStart = useCallback(() => {
    edgeReconnectSuccessful.current = false;
  }, []);

  const onEdgeUpdate = useCallback((oldEdge, newConnection) => {
    edgeReconnectSuccessful.current = true;
    setEdges(els => reconnectEdge(oldEdge, newConnection, els));
  }, [setEdges]);

  const onEdgeUpdateEnd = useCallback((_, edge) => {
    if (!edgeReconnectSuccessful.current) {
      setEdges(eds => eds.filter(e => e.id !== edge.id));
    }
    edgeReconnectSuccessful.current = true;
  }, [setEdges]);

  return { onConnect, onEdgeUpdateStart, onEdgeUpdate, onEdgeUpdateEnd };
};