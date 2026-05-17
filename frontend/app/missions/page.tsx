"use client";

import { useEffect, useState } from "react";
import { Search, Filter, Plus, MoreVertical } from "lucide-react";
import Link from "next/link";

interface Mission {
  id: string;
  name: string;
  status: string;
  protocol: string;
  security_level: string;
  last_updated: string;
}

export default function MissionsPage() {
  const [missions, setMissions] = useState<Mission[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would fetch from http://localhost:8081/missions
    // For now, I'll use mock data to ensure the UI looks good immediately
    const mockMissions: Mission[] = [
      { id: "1", name: "Project Aurora", status: "In Progress", protocol: "BB84", security_level: "High", last_updated: "2023-10-25 14:30" },
      { id: "2", name: "Deep Space Relay", status: "Completed", protocol: "E91", security_level: "Critical", last_updated: "2023-10-24 09:15" },
      { id: "3", name: "Shadow Link", status: "Warning", protocol: "BB84+E", security_level: "Medium", last_updated: "2023-10-23 18:45" },
      { id: "4", name: "Cyber Shield", status: "In Progress", protocol: "BB84", security_level: "High", last_updated: "2023-10-22 11:20" },
      { id: "5", name: "Nebula Protocol", status: "Draft", protocol: "BB84", security_level: "Low", last_updated: "2023-10-21 16:00" },
    ];
    
    setMissions(mockMissions);
    setLoading(false);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Missions</h1>
          <p className="text-slate-500 dark:text-slate-400">
            Manage and monitor all quantum-safe communication missions.
          </p>
        </div>
        <Link 
          href="/missions/new"
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
        >
          <Plus size={20} className="mr-2" />
          New Mission
        </Link>
      </div>

      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input 
            type="text" 
            placeholder="Search missions..." 
            className="w-full pl-10 pr-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          />
        </div>
        <button className="flex items-center px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
          <Filter size={18} className="mr-2 text-slate-500" />
          Filter
        </button>
      </div>

      <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-slate-500">Loading missions...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50">
                  <th className="px-6 py-4 font-medium text-slate-500">Mission Name</th>
                  <th className="px-6 py-4 font-medium text-slate-500">Status</th>
                  <th className="px-6 py-4 font-medium text-slate-500">Protocol</th>
                  <th className="px-6 py-4 font-medium text-slate-500">Security</th>
                  <th className="px-6 py-4 font-medium text-slate-500">Last Updated</th>
                  <th className="px-6 py-4 font-medium text-slate-500 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {missions.map((mission) => (
                  <tr key={mission.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/50 transition-colors">
                    <td className="px-6 py-4 font-medium">{mission.name}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={mission.status} />
                    </td>
                    <td className="px-6 py-4 text-slate-500">{mission.protocol}</td>
                    <td className="px-6 py-4">
                      <SecurityBadge level={mission.security_level} />
                    </td>
                    <td className="px-6 py-4 text-slate-500 text-sm">{mission.last_updated}</td>
                    <td className="px-6 py-4 text-right">
                      <button className="p-1 hover:bg-slate-200 dark:hover:bg-slate-700 rounded transition-colors">
                        <MoreVertical size={18} className="text-slate-400" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    "In Progress": "bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400",
    "Completed": "bg-emerald-50 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400",
    "Warning": "bg-amber-50 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400",
    "Draft": "bg-slate-50 text-slate-600 dark:bg-slate-800 dark:text-slate-400",
  };

  return (
    <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${colors[status] || colors["Draft"]}`}>
      {status}
    </span>
  );
}

function SecurityBadge({ level }: { level: string }) {
  const colors: Record<string, string> = {
    "Critical": "text-purple-600 bg-purple-50 dark:bg-purple-900/30 dark:text-purple-400",
    "High": "text-blue-600 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-400",
    "Medium": "text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 dark:text-emerald-400",
    "Low": "text-slate-600 bg-slate-50 dark:bg-slate-800 dark:text-slate-400",
  };

  return (
    <span className={`text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded ${colors[level] || colors["Low"]}`}>
      {level}
    </span>
  );
}
