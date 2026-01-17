"use client";

import React, { useState, useCallback } from "react";
import { Upload, FileText, Brain, User, Briefcase, Cloud, CheckCircle, Sparkles, XCircle, GraduationCap, ChevronRight } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent, dragging: boolean) => {
    e.preventDefault(); e.stopPropagation(); setIsDragging(dragging);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault(); e.stopPropagation(); setIsDragging(false);
    if (e.dataTransfer.files?.[0]) validateFile(e.dataTransfer.files[0]);
  }, []);

  const validateFile = (f: File) => {
    if (f.type !== "application/pdf") return setError("Only PDF files allowed ⚠️");
    setFile(f); setError(""); setResult(null);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true); setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/analyze", { method: "POST", body: formData });
      if (!res.ok) throw new Error("Failed to analyze resume");
      const data = await res.json();
      if(data.error) throw new Error(data.error);
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 bg-grid-pattern relative overflow-x-hidden font-sans text-slate-800">
      
      {/* Background Blobs (Decoration) */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-400/20 rounded-full blur-3xl -z-10 animate-pulse"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl -z-10 animate-pulse delay-1000"></div>

      <div className="py-16 px-4">
        
        {/* Header Section */}
        <div className="max-w-4xl mx-auto text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/50 border border-blue-100 text-blue-600 text-sm font-semibold mb-6 shadow-sm animate-fade-in-up">
            <Sparkles size={16} /> AI-Powered Resume Analysis
          </div>
          <h1 className="text-5xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-900 via-blue-800 to-slate-900 mb-6 drop-shadow-sm tracking-tight animate-fade-in-up">
            Unlock Your Career <br/> Potential
          </h1>
          <p className="text-slate-500 text-lg md:text-xl max-w-2xl mx-auto animate-fade-in-up">
            Upload your resume and let our advanced AI extract skills, experience, and classify your ideal role instantly.
          </p>
        </div>

        {/* Upload Section */}
        <div className="max-w-2xl mx-auto w-full mb-20 animate-fade-in-up">
          <div 
            className={`relative group border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300 cursor-pointer glass-card
              ${isDragging ? "border-blue-500 bg-blue-50/50 scale-[1.02]" : "border-slate-300 hover:border-blue-400 hover:shadow-2xl"}`}
            onDragOver={(e) => handleDrag(e, true)}
            onDragLeave={(e) => handleDrag(e, false)}
            onDrop={handleDrop}
          >
            <input type="file" accept=".pdf" onChange={(e) => e.target.files?.[0] && validateFile(e.target.files[0])} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"/>
            
            <div className="flex flex-col items-center pointer-events-none relative z-20">
              {file ? (
                <div className="animate-fade-in-up">
                  <div className="w-20 h-20 bg-gradient-to-tr from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center mb-6 mx-auto shadow-lg shadow-blue-500/30">
                    <FileText size={40} className="text-white" />
                  </div>
                  <p className="text-2xl font-bold text-slate-800">{file.name}</p>
                  <p className="text-green-600 font-medium mt-2 flex items-center justify-center gap-2 bg-green-50 px-4 py-1 rounded-full inline-block">
                    <CheckCircle size={16}/> Ready for analysis
                  </p>
                </div>
              ) : (
                <div className="group-hover:-translate-y-2 transition-transform duration-300">
                  <div className={`w-20 h-20 rounded-2xl flex items-center justify-center mb-6 mx-auto transition-all shadow-lg
                    ${isDragging ? "bg-blue-500 text-white" : "bg-white text-blue-600 shadow-blue-100"}`}>
                    <Cloud size={40} className="animate-float" />
                  </div>
                  <p className="text-2xl font-bold text-slate-700 mb-2">Drag & Drop Resume</p>
                  <p className="text-slate-400">Supported format: PDF</p>
                </div>
              )}
            </div>
          </div>

          <button 
            onClick={handleAnalyze} disabled={!file || loading}
            className={`mt-8 w-full py-5 rounded-2xl text-white font-bold text-xl shadow-xl transition-all transform duration-300
              ${!file || loading ? "bg-slate-300 cursor-not-allowed shadow-none" : "bg-gradient-to-r from-blue-600 to-indigo-700 animate-gradient hover:scale-[1.02] hover:shadow-blue-500/40 active:scale-95"}`}
          >
            {loading ? (
               <span className="flex items-center justify-center gap-3">
                 <div className="w-6 h-6 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
                 Processing...
               </span>
            ) : "Analyze My Resume"}
          </button>

          {error && (
            <div className="mt-6 p-4 bg-red-50 text-red-600 rounded-xl flex items-center gap-3 border border-red-100 animate-shake shadow-sm">
              <XCircle size={24} className="flex-shrink-0"/> <span className="font-medium">{error}</span>
            </div>
          )}
        </div>

        {/* Results Dashboard */}
        {result && (
          <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-6 animate-fade-in-up pb-20">
            
            {/* 1. Classification (Large Card) */}
            <div className="md:col-span-7 glass-card p-8 rounded-3xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
                <Brain size={120} className="text-blue-600"/>
              </div>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-blue-100 rounded-xl text-blue-600"><Brain size={24}/></div>
                <h3 className="font-bold text-slate-500 uppercase tracking-wider text-sm">Role Classification</h3>
              </div>
              <h2 className="text-4xl md:text-5xl font-black text-slate-800 mb-8">{result.classification}</h2>
              <div className="bg-white/60 p-5 rounded-2xl border border-white/60">
                <div className="flex justify-between text-sm font-bold text-slate-600 mb-2">
                  <span>AI Confidence Match</span>
                  <span>{(result.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-4 overflow-hidden">
                  <div 
                    className={`h-full rounded-full transition-all duration-1000 ease-out ${result.confidence > 0.8 ? 'bg-gradient-to-r from-green-400 to-green-600' : 'bg-gradient-to-r from-yellow-400 to-yellow-600'}`} 
                    style={{ width: `${result.confidence * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* 2. Experience (Side Card) */}
            <div className="md:col-span-5 glass-card p-8 rounded-3xl relative overflow-hidden group flex flex-col justify-between">
               <div className="absolute -bottom-4 -right-4 w-32 h-32 bg-purple-100 rounded-full blur-2xl group-hover:bg-purple-200 transition-colors"></div>
               <div>
                  <div className="flex items-center gap-3 mb-6">
                    <div className="p-3 bg-purple-100 rounded-xl text-purple-600"><Briefcase size={24}/></div>
                    <h3 className="font-bold text-slate-500 uppercase tracking-wider text-sm">Experience</h3>
                  </div>
                  <div className="flex items-baseline gap-2 mb-2">
                    <span className="text-6xl font-black text-slate-900 tracking-tight">{result.experience_years}</span>
                    <span className="text-xl font-medium text-slate-400">Years</span>
                  </div>
               </div>
               <div className={`self-start px-6 py-2 rounded-xl font-bold text-sm tracking-wide uppercase shadow-sm
                  ${result.experience_level === 'Senior' ? 'bg-purple-100 text-purple-700' : result.experience_level === 'Mid' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'}`}>
                  {result.experience_level} Level
               </div>
            </div>

            {/* 3. Candidate Info & Education */}
            <div className="md:col-span-12 grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Personal Info */}
              <div className="glass-card p-8 rounded-3xl">
                 <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-200/60">
                    <User size={24} className="text-slate-400"/> <h3 className="font-bold text-slate-700">Candidate Details</h3>
                 </div>
                 <ul className="space-y-5">
                    <li className="flex justify-between items-center group">
                      <span className="text-sm text-slate-400 font-semibold uppercase">Name</span>
                      <span className="font-bold text-lg text-slate-800 group-hover:text-blue-600 transition-colors">{result.name}</span>
                    </li>
                    <li className="flex justify-between items-center group">
                      <span className="text-sm text-slate-400 font-semibold uppercase">Email</span>
                      <span className="font-medium text-slate-800 break-all group-hover:text-blue-600 transition-colors">{result.email || "N/A"}</span>
                    </li>
                    <li className="flex justify-between items-center group">
                      <span className="text-sm text-slate-400 font-semibold uppercase">Phone</span>
                      <span className="font-medium text-slate-800 group-hover:text-blue-600 transition-colors">{result.phone || "N/A"}</span>
                    </li>
                 </ul>
              </div>

              {/* Education */}
              <div className="glass-card p-8 rounded-3xl">
                 <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-200/60">
                    <GraduationCap size={24} className="text-slate-400"/> <h3 className="font-bold text-slate-700">Education</h3>
                 </div>
                 {result.education && result.education.length > 0 ? (
                   <div className="space-y-4">
                     {result.education.map((edu: string, idx: number) => (
                       <div key={idx} className="flex items-start gap-4">
                         <div className="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 mt-1">
                            <span className="w-2.5 h-2.5 bg-blue-500 rounded-full"></span>
                         </div>
                         <p className="font-semibold text-slate-700 leading-relaxed">{edu}</p>
                       </div>
                     ))}
                   </div>
                 ) : (
                   <div className="h-full flex flex-col items-center justify-center text-slate-400 italic opacity-60">
                      <GraduationCap size={40} className="mb-2"/>
                      No education details detected
                   </div>
                 )}
              </div>
            </div>

            {/* 4. Skills Grid */}
            <div className="md:col-span-12 glass-card p-8 rounded-3xl">
              <div className="flex items-center gap-3 mb-8">
                 <div className="p-2 bg-indigo-100 rounded-lg text-indigo-600"><CheckCircle size={20}/></div>
                 <h3 className="font-bold text-slate-700 uppercase tracking-wide">Top Technical Skills</h3>
              </div>
              {result.skills.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {result.skills.map((skill: string, idx: number) => (
                    <div 
                      key={idx} 
                      className="flex items-center gap-3 p-4 bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md hover:border-indigo-300 hover:-translate-y-1 transition-all duration-200 group"
                    >
                      <span className="flex items-center justify-center w-8 h-8 bg-slate-100 text-slate-500 text-xs font-bold rounded-lg flex-shrink-0 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                        {idx + 1}
                      </span>
                      <span className="font-bold text-slate-700 text-sm truncate group-hover:text-indigo-700 transition-colors" title={skill}>
                        {skill}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-400 italic text-center py-8">No specific skills detected</p>
              )}
            </div>

          </div>
        )}
      </div>
    </div>
  );
}