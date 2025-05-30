import { useState, useEffect } from 'react';

export const useFlowData = () => {
  const [functionDict, setFunctionDict] = useState(null);
  const [functionList, setFunctionList] = useState([]);
  const [functionDefinitions, setFunctionDefinitions] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dictRes, listRes, funcRes] = await Promise.all([
          fetch("http://localhost:8000/function_dict"),
          fetch("http://localhost:8000/function_list"),
          fetch("http://localhost:8000/get_functions")
        ]);
        
        setFunctionDict(await dictRes.json());
        setFunctionList(await listRes.json());
        setFunctionDefinitions(await funcRes.json());
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);
  
  return { functionDict, functionList, functionDefinitions };
};