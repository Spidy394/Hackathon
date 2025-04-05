import React from "react";
import { Plus, Search, Trash2, FastForward, Upload, Download, FileText } from "lucide-react";
import ActionCard from "../../shared/ActionCard";
import HText from "../../shared/HText"

const Management = () => {

  return (
    <div className="flex flex-col items-center mt-10 px-4">
      <HText>Cargo Management Dashboard</HText>
      
      <div className="flex flex-wrap justify-center gap-6">
        <ActionCard icon={<Plus />} label="Placement" />
        <ActionCard icon={<Search />} label="Retrieve" />
        <ActionCard icon={<Trash2 />} label="Dispose" />
        <ActionCard icon={<FastForward />} label="Simulate" />
        <ActionCard icon={<Download />} label="Load CSV" />
        <ActionCard icon={<Upload />} label="Export CSV" />
        <ActionCard icon={<FileText />} label="Log File" />
      </div>
    </div>
  );
};

export default Management;
