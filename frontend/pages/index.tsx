"use client";
import { useState, useRef } from "react";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { InteractiveGradientBackground } from "@/components/ui/interactive-gradient-background";
import { ShimmerButton } from "@/components/ui/shimmer-button";
import { cn } from "@/lib/utils";

export default function Home() {
  const [pdfUrl, setPdfUrl] = useState<string>("");
  const [messages, setMessages] = useState<string[]>([]);
  const [latestInput, setLatestInput] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  async function handleChatSubmit(value: string) {
    setMessages((msgs) => [...msgs, value]);
    setLatestInput("");
    let jobUrl = "";
    let basicDetails = "";
    if (/(https?:\/\/[^ ]+)/.test(value)) jobUrl = value;
    else basicDetails = value;
    const formData = new FormData();
    if (resumeFile) formData.append("resume_file", resumeFile);
    if (basicDetails) formData.append("basic_details", basicDetails);
    if (jobUrl) formData.append("job_urls", jobUrl);

    try {
      const res = await fetch("http://localhost:8000/process/", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        alert("Resume creation failed! Please try again.");
        return;
      }
      const blob = await res.blob();
      setPdfUrl(URL.createObjectURL(blob));
    } catch (err) {
      console.error(err);
      alert("Network error when creating resume. Is the backend running?");
    }
  }

  return (
    <InteractiveGradientBackground intensity={1}>
      <div className="min-h-screen flex flex-col items-center justify-center px-4 py-20">
        {/* Main heading */}
        <div className="mb-16 text-center">
          <h1 className="text-6xl md:text-8xl font-bold text-white drop-shadow-2xl" style={{ fontFamily: 'system-ui, -apple-system, sans-serif', letterSpacing: '-0.02em' }}>
            AI Resume Builder
          </h1>
          <p className="text-xl md:text-2xl text-white/90 mt-4 font-light">
            Create your perfect resume in seconds
          </p>
        </div>

        {/* Centered content container */}
        <div className="w-full max-w-2xl flex flex-col items-center space-y-6">
          {/* Message list */}
          {messages.length > 0 && (
            <div className="w-full flex flex-col space-y-3 mb-4">
              {messages.map((msg, i) => (
                <div 
                  key={i} 
                  className="px-6 py-3 rounded-full bg-white/10 backdrop-blur-md text-white text-sm sm:text-base shadow-lg max-w-xl mx-auto border border-white/20"
                >
                  {msg}
                </div>
              ))}
            </div>
          )}

          {/* Chat input with vanishing effect */}
          <div className="w-full">
            <PlaceholdersAndVanishInput
              placeholders={[
                "Who is Tyler Durden?",
                "Type your resume details here...",
                "Paste a job description link...",
                "Describe your work experience...",
              ]}
              onChange={(e) => setLatestInput(e.target.value)}
              onSubmit={(e) => {
                e.preventDefault();
                if (latestInput.trim()) handleChatSubmit(latestInput.trim());
              }}
            />
          </div>

          {/* Shimmer button for file upload */}
          <div className="w-full max-w-md mx-auto">
            <ShimmerButton
              onClick={() => fileInputRef.current?.click()}
              className="w-full text-base font-medium"
              background="rgba(0, 0, 0, 0.7)"
              shimmerColor="#ffffff"
              borderRadius="9999px"
            >
              📄 Upload Resume
            </ShimmerButton>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
              className="hidden"
            />
            {resumeFile && (
              <div className="text-white text-sm mt-3 text-center font-medium bg-white/10 backdrop-blur-md rounded-full px-4 py-2 border border-white/20">
                ✓ {resumeFile.name}
              </div>
            )}
          </div>

          {/* PDF Preview & Download */}
          {pdfUrl && (
            <div className="mt-12 w-full bg-white/10 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20">
              <div className="mb-6">
                <h2 className="text-2xl font-semibold text-white text-center">
                  Your Generated Resume
                </h2>
              </div>
              <iframe 
                src={pdfUrl} 
                width="100%" 
                height="600px" 
                className="rounded-2xl border-0 shadow-2xl"
              />
              <div className="mt-8 w-full max-w-md mx-auto">
                <a href={pdfUrl} download="resume.pdf">
                  <ShimmerButton 
                    className="w-full text-base font-medium"
                    background="rgba(0, 0, 0, 0.7)"
                    borderRadius="9999px"
                  >
                    ⬇️ Download PDF Resume
                  </ShimmerButton>
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </InteractiveGradientBackground>
  );
}