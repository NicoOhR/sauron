import { useState, useEffect, useCallback } from 'react';

import { CursorGradient } from './components/radial-gradient';
import { ReactFlow, Background, applyNodeChanges, type OnNodesChange, type Node, type Edge } from '@xyflow/react';
import { LineChart, Line, CartesianGrid } from 'recharts';

import { Separator } from "@/components/ui/separator";
import { ZoomSlider } from "@/components/zoom-slider";
import {LatencyTable} from './components/latency-table';

import '@xyflow/react/dist/style.css';

// Some list of nodes with ids and their names
const nodeList = [
  { "id": 0, "name": "rcev" },
  { "id": 1, "name": "process" },
  { "id": 2, "name": "send" },
  { "id": 3, "name": "done"},

]
// Some list of how nodes are connected
const vertexList = [
  { "start": 0, "trace": 0, "end": 1 },
  { "start": 1, "trace": 0, "end": 2 },
  { "start": 2, "trace": 0, "end": 3 },
]

// Creates setup for positioning the nodes
var initialNodes: Node[] = []
var initialEdges: Edge[] = []
var nodeIdToName = new Map();
var objectParents = {}
var layers = {}
var maxLayer = 0
// Creates each node
nodeList.forEach((node) => {
  let nodeId = node.id.toString()
  let nodeName = node.name
  initialNodes.push({ id: nodeId, position: { x: 0, y: 0 }, data: { label: nodeName }, style: { border: '1px solid #52525b' } })
  nodeIdToName.set(nodeId, nodeName);
  objectParents[nodeId] = [];
  layers[nodeId] = 0;
})
// Creates each vertex, setting up children to move down
vertexList.forEach((vertex) => {
  let start = vertex.start.toString()
  let end = vertex.end.toString()
  let edgeId = `${start}-${end}`
  initialEdges.push({ id: edgeId, source: start, target: end,  style: { stroke: '#52525b', animation: "none", strokeDasharray: 5 } })
  objectParents[edgeId] = [start]
  objectParents[end].push(edgeId)
  layers[end] = layers[start] >= layers[end] ? layers[start] + 1 : layers[end]
  if (layers[end] > maxLayer) { maxLayer = layers[end] }
})

var layerX = Array(maxLayer + 1).fill(1);

// Actually move down children
initialNodes = initialNodes.map((n) => ({ ...n, position: { x: layerX[layers[n.id]]++ * 200, y: layers[n.id] * 200 } }))

let data_var = [{ uv: 100 }, { uv: 300 }, { uv: 250 }, { uv: 200 }, { uv: 400 }, { uv: 200 }, { uv: 80 }, { uv: 150 }, { uv: 190 }];

function App() {
  const [data, setData] = useState(data_var);
  // Keep track of the nodes and edges
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [selectedIDs, setSelectedIDs] = useState<String[]>([]);

  // Allow nodes to be able to be moved
  const onNodesChange: OnNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [setNodes],
  );

  // Update the path whenever a node/edge is clicked
  const onObjectClicked = (_event: React.MouseEvent, object: Node | Edge) => {
    setData((data) => {
      const newData = [...data];
      newData.push({ uv: Math.random() * 500 });
      return newData.slice(-10);
    });
    let connections: string[] = [];
    if (selectedIDs.length == 0 || selectedIDs[0] != object.id) {
      let queue = [object.id]
      while (queue.length != 0) {
        let item = queue.shift();
        connections.push(item)
        objectParents[item].forEach((parent: string) => queue.push(parent))
      }
    }
    // Updates the theme of each node
    setNodes((nds) =>
      nds.map((n) => (connections.includes(n.id) ? { ...n, style: { border: '1px solid #6366f1' } } : { ...n, style: { border: '1px solid #52525b' } }))
    );
    setEdges((eds) =>
      eds.map((e) => (connections.includes(e.id) ? { ...e, style: { stroke: '#6366f1', animation: "dashdraw 0.1s linear infinite", strokeDasharray: 5 } }
        : { ...e, style: { stroke: '#52525b', animation: "none", strokeDasharray: 5 } }))
    );
    setSelectedIDs(connections)
  };

  const startView = {
    padding: 0.25
  }

  console.log(selectedIDs)

  return (
    <body className="w-screen h-screen p-3 bg-zinc-950 text-zinc-200">
      <CursorGradient />
      <header className="w-full h-20 flex flex-row  ">
        <h2 className="p-4 pr-0 text-zinc-600 text-2xl font-extrabold tracking-tight">
          {'> '}
        </h2>
        <h2 className="p-4 text-zinc-100 text-3xl font-semibold tracking-tight">
          Sauron
        </h2>
      </header>
      <Separator />
      <main className="w-full h-[calc(100%-5rem)] pt-3 flex flex-row gap-3">
        <div className="w-2/3 h-full">
          <ReactFlow colorMode="dark" nodes={nodes} edges={edges} onNodesChange={onNodesChange} onNodeClick={onObjectClicked} onEdgeClick={onObjectClicked} fitView fitViewOptions={startView}>
            <Background color="#52525b" style={{ background: "#09090b" }} gap={12} size={1} />
            <ZoomSlider position="bottom-left" />
          </ReactFlow>
        </div>
        <Separator orientation="vertical" />
        <div className="w-1/3 flex flex-col gap-3 overflow-x-hidden overflow-y-auto no-scrollbar">
          <div className="w-full min-h-60 h-full overflow-x-hidden overflow-y-auto no-scrollbar">
            <LatencyTable selectedIDs={selectedIDs}/>
          </div>
          <Separator />
          <div className="w-full flex justify-center p-3 flex flex-col gap-3">
            <h4 className="text-zinc-100 text-xl font-semibold tracking-tight">
              p99 latency
            </h4>
            <LineChart width={500} height={300} data={data}>
              <CartesianGrid stroke="#27272a" strokeDasharray="5 5" />
              <Line type="monotone" dataKey="uv" stroke="#6366f1" />
            </LineChart>
          </div>
           <div className="w-full flex justify-center p-3 flex flex-col gap-3">
            <h4 className="text-zinc-100 text-xl font-semibold tracking-tight">
              Data Transfer For #{selectedIDs && selectedIDs[0]}
            </h4>
            <LineChart width={500} height={300} data={data}>
              <CartesianGrid stroke="#27272a" strokeDasharray="5 5" />
              <Line type="monotone" dataKey="uv" stroke="#6366f1" />
            </LineChart>
          </div>
           <div className="w-full flex justify-center p-3 flex flex-col gap-3">
            <h4 className="text-zinc-100 text-xl font-semibold tracking-tight">
              Data Transfer For #{selectedIDs && selectedIDs[0]}
            </h4>
            <LineChart width={500} height={300} data={data}>
              <CartesianGrid stroke="#27272a" strokeDasharray="5 5" />
              <Line type="monotone" dataKey="uv" stroke="#6366f1" />
            </LineChart>
          </div>
        </div>
      </main>
    </body>
  )
}

export default App
