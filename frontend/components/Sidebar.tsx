"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Rocket, 
  Cpu, 
  ShieldCheck, 
  BarChart3, 
  Settings,
  Menu,
  X
} from "lucide-react";
import { useState } from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const navItems = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Missions", href: "/missions", icon: Rocket },
  { name: "Quantum Circuits", href: "/quantum", icon: Cpu },
  { name: "Security Policies", href: "/policies", icon: ShieldCheck },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
];

export function Sidebar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(true);

  return (
    <>
      <button 
        className="fixed top-4 left-4 z-50 p-2 bg-white rounded-md shadow-md lg:hidden"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      <div className={cn(
        "fixed inset-y-0 left-0 z-40 w-64 bg-slate-900 text-white transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-center h-20 border-b border-slate-800">
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              QuantumSafe
            </h1>
          </div>
          
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors",
                    isActive 
                      ? "bg-blue-600 text-white" 
                      : "text-slate-400 hover:bg-slate-800 hover:text-white"
                  )}
                >
                  <Icon className="mr-3" size={20} />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          <div className="p-4 border-t border-slate-800">
            <button className="flex items-center w-full px-4 py-3 text-sm font-medium text-slate-400 rounded-lg hover:bg-slate-800 hover:text-white transition-colors">
              <Settings className="mr-3" size={20} />
              Settings
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
