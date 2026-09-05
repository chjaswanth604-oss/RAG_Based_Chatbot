import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FileText, Users, HelpCircle, CheckCircle, AlertTriangle, Upload, ArrowLeft, RefreshCw, Layers } from 'lucide-react';
import { adminService } from '../services/api';
import { useAuth } from '../context/AuthContext';

const AdminDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const res = await adminService.getStats();
      setStats(res.data);
    } catch (err) {
      console.error("Failed to fetch admin stats:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-10">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header Bar */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Link to="/chat" className="text-xs text-indigo-400 hover:underline flex items-center gap-1">
                <ArrowLeft className="w-3.5 h-3.5" /> Back to Chat
              </Link>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Admin Knowledge Base Control Center
            </h1>
            <p className="text-sm text-slate-400">
              Overview statistics and document processing metrics
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={fetchStats}
              className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white transition-colors"
              title="Refresh Statistics"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={() => navigate('/admin/documents')}
              className="flex items-center gap-2 py-2.5 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-semibold text-sm transition-all shadow-lg shadow-indigo-600/30 glow-primary"
            >
              <Upload className="w-4 h-4" />
              Manage & Upload Documents
            </button>
          </div>
        </div>

        {/* Metrics Grid */}
        {loading ? (
          <div className="py-12 text-center text-slate-500 text-sm animate-pulse">
            Loading analytics dashboard...
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {/* Total Documents */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Documents</p>
                <h3 className="text-3xl font-extrabold text-white mt-1">{stats?.total_documents || 0}</h3>
              </div>
              <div className="p-3 rounded-2xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                <FileText className="w-6 h-6" />
              </div>
            </div>

            {/* Total Registered Students */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Students</p>
                <h3 className="text-3xl font-extrabold text-white mt-1">{stats?.total_students || 0}</h3>
              </div>
              <div className="p-3 rounded-2xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
                <Users className="w-6 h-6" />
              </div>
            </div>

            {/* Total Questions Asked */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Queries Answered</p>
                <h3 className="text-3xl font-extrabold text-white mt-1">{stats?.total_questions || 0}</h3>
              </div>
              <div className="p-3 rounded-2xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <HelpCircle className="w-6 h-6" />
              </div>
            </div>

            {/* Documents Successfully Processed */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Processed Status</p>
                <h3 className="text-3xl font-extrabold text-emerald-400 mt-1">{stats?.documents_processed || 0}</h3>
              </div>
              <div className="p-3 rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <CheckCircle className="w-6 h-6" />
              </div>
            </div>

            {/* Documents Failed */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Processing Failures</p>
                <h3 className="text-3xl font-extrabold text-rose-400 mt-1">{stats?.processing_failed || 0}</h3>
              </div>
              <div className="p-3 rounded-2xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <AlertTriangle className="w-6 h-6" />
              </div>
            </div>

            {/* Quick Action Navigation Card */}
            <div
              onClick={() => navigate('/admin/documents')}
              className="glass-panel p-6 rounded-2xl border border-indigo-500/30 bg-indigo-950/20 hover:bg-indigo-950/40 cursor-pointer transition-all flex items-center justify-between group"
            >
              <div>
                <p className="text-xs font-semibold text-indigo-300 uppercase tracking-wider">Knowledge Base</p>
                <h3 className="text-lg font-bold text-white mt-1 group-hover:text-indigo-300 transition-colors">
                  Upload & Delete Documents →
                </h3>
              </div>
              <div className="p-3 rounded-2xl bg-indigo-600 text-white">
                <Layers className="w-6 h-6" />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
