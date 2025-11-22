import React, { useRef, useEffect, useState } from "react";
import ForceGraph3D from "react-force-graph-3d";
import * as THREE from "three";
import { fetchGraphData } from "../api";   // <-- integrated API call

export default function NodeMap() {
  const fgRef = useRef();
  const [data, setData] = useState({ nodes: [], links: [] });

  // -------------------------------------------------
  // LOAD GRAPH FROM BACKEND
  // -------------------------------------------------
  useEffect(() => {
    async function loadGraph() {
      try {
        const res = await fetchGraphData();
        setData(res.data);
      } catch (err) {
        console.error("Graph backend missing, using fallback.");

        // fallback synthetic graph for UI preview
        const nodes = Array.from({ length: 20 }).map((_, i) => ({
          id: `N${i}`,
          val: Math.random() * 8 + 1,
          group: i % 4,
        }));

        const links = [];
        for (let i = 0; i < 30; i++) {
          links.push({
            source: `N${Math.floor(Math.random() * 20)}`,
            target: `N${Math.floor(Math.random() * 20)}`,
          });
        }

        setData({ nodes, links });
      }
    }

    loadGraph();
  }, []);

  // -------------------------------------------------
  // RENDER
  // -------------------------------------------------
  return (
    <div className="h-[90vh] glass rounded-xl p-2">
      <div className="flex justify-between items-center mb-2">
        <h3 className="neon-title">3D Tactical Network Map</h3>
        <div className="text-xs text-slate-400">Radar sweep active</div>
      </div>

      <div style={{ height: "80vh" }}>
        <ForceGraph3D
          ref={fgRef}
          graphData={data}
          nodeAutoColorBy="group"
          nodeRelSize={3}
          backgroundColor="#071018"
          linkWidth={1}
          linkColor={() => "rgba(0,255,255,0.2)"}
          
          nodeThreeObject={(node) => {
            const geometry = new THREE.SphereGeometry(1.2, 16, 16);
            const material = new THREE.MeshBasicMaterial({
              color:
                node.group === 0
                  ? 0x00f0ff
                  : node.group === 1
                  ? 0xb04bff
                  : node.group === 2
                  ? 0xff9f43
                  : 0xff3b3b,
            });
            return new THREE.Mesh(geometry, material);
          }}

          onNodeClick={(node) => {
            fgRef.current.centerAt(node.x, node.y, node.z, 600);
            fgRef.current.zoom(4, 600);
          }}
        />
      </div>
    </div>
  );
}
