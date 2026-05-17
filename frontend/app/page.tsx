import { 
  Rocket, 
  ShieldCheck, 
  Activity, 
  AlertCircle,
  Plus
} from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-slate-500 dark:text-slate-400">
            Welcome to the Quantum-Safe Mission Communications Planner.
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

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Active Missions" 
          value="12" 
          icon={<Rocket className="text-blue-500" size={24} />} 
          change="+2 from last week"
        />
        <StatCard 
          title="Security Level" 
          value="Quantum-Safe" 
          icon={<ShieldCheck className="text-emerald-500" size={24} />} 
          change="All protocols compliant"
        />
        <StatCard 
          title="System Health" 
          value="98.2%" 
          icon={<Activity className="text-purple-500" size={24} />} 
          change="Operational"
        />
        <StatCard 
          title="Active Threats" 
          value="0" 
          icon={<AlertCircle className="text-slate-400" size={24} />} 
          change="No incidents detected"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Missions</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-100 dark:border-slate-800">
                  <th className="pb-3 font-medium text-slate-500">Mission Name</th>
                  <th className="pb-3 font-medium text-slate-500">Status</th>
                  <th className="pb-3 font-medium text-slate-500">Protocol</th>
                  <th className="pb-3 font-medium text-slate-500 text-right">Last Updated</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                <MissionRow name="Project Aurora" status="In Progress" protocol="BB84" updated="2h ago" />
                <MissionRow name="Deep Space Relay" status="Completed" protocol="E91" updated="5h ago" />
                <MissionRow name="Shadow Link" status="Warning" protocol="BB84+E" updated="1d ago" />
                <MissionRow name="Cyber Shield" status="In Progress" protocol="BB84" updated="2d ago" />
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Links</h2>
          <div className="space-y-4">
            <QuickLink href="/quantum" title="Circuit Simulator" description="Test your quantum protocols before deployment." />
            <QuickLink href="/policies" title="Policy Manager" description="Update and verify security requirements." />
            <QuickLink href="/analytics" title="Network Health" description="Monitor real-time system performance." />
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, change }: { title: string, value: string, icon: React.ReactNode, change: string }) {
  return (
    <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-slate-50 dark:bg-slate-800 rounded-lg">
          {icon}
        </div>
        <span className="text-xs font-medium text-emerald-500 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-1 rounded">
          {change.includes("+") ? change : "Stable"}
        </span>
      </div>
      <div>
        <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</h3>
        <p className="text-2xl font-bold">{value}</p>
      </div>
    </div>
  );
}

function MissionRow({ name, status, protocol, updated }: { name: string, status: string, protocol: string, updated: string }) {
  const statusColors = {
    "In Progress": "bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400",
    "Completed": "bg-emerald-50 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400",
    "Warning": "bg-amber-50 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400",
  };

  return (
    <tr>
      <td className="py-4 font-medium">{name}</td>
      <td className="py-4">
        <span className={`text-xs px-2 py-1 rounded-full ${statusColors[status as keyof typeof statusColors]}`}>
          {status}
        </span>
      </td>
      <td className="py-4 text-slate-500">{protocol}</td>
      <td className="py-4 text-right text-slate-400 text-sm">{updated}</td>
    </tr>
  );
}

function QuickLink({ href, title, description }: { href: string, title: string, description: string }) {
  return (
    <Link href={href} className="block group">
      <div className="p-4 rounded-lg border border-slate-100 dark:border-slate-800 hover:border-blue-200 dark:hover:border-blue-900 transition-colors bg-slate-50/50 dark:bg-slate-800/50 group-hover:bg-blue-50/50 dark:group-hover:bg-blue-900/20">
        <h3 className="font-medium group-hover:text-blue-600 transition-colors">{title}</h3>
        <p className="text-sm text-slate-500 dark:text-slate-400">{description}</p>
      </div>
    </Link>
  );
}
