import React from 'react';

export default function CandidateList({candidates}){
  return (
    <div className="mt-4">
      <h3 className="text-lg">Candidates</h3>
      <ul>
        {candidates.map((c, i) => (
          <li key={i} className="p-2 border-b border-gray-700">
            <div className="font-mono text-sm">{c[0]}</div>
            <div>{c[1]} — Score: {(c[2]||0).toFixed(3)}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
