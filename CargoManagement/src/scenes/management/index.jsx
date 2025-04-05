import React, { useState } from "react";
import {
  Plus,
  Search,
  Trash2,
  FastForward,
  Upload,
  Download,
  FileText,
} from "lucide-react";

import ActionCard from "../../shared/ActionCard";
import HText from "../../shared/HText";

import PlacementSection from "./PlacementSection";
import SearchSection from "./SearchSection";
import DisposeSection from "./DisposeSection";
import SimulateSection from "./SimulateSection";
import LoadCSVSection from "./LoadCSVSection";
import ExportCSVSection from "./ExportCSVSection";
import LogSection from "./LogSection";

const ACTIONS = [
  { label: "Placement", icon: <Plus />, component: <PlacementSection /> },
  { label: "Retrieve", icon: <Search />, component: <SearchSection /> },
  { label: "Dispose", icon: <Trash2 />, component: <DisposeSection /> },
  { label: "Simulate", icon: <FastForward />, component: <SimulateSection /> },
  { label: "Load CSV", icon: <Download />, component: <LoadCSVSection /> },
  { label: "Export CSV", icon: <Upload />, component: <ExportCSVSection /> },
  { label: "Log File", icon: <FileText />, component: <LogSection /> },
];

const Management = () => {
  const [selectedAction, setSelectedAction] = useState(null);

  const currentComponent = ACTIONS.find(
    (action) => action.label === selectedAction
  )?.component;

  return (
    <div className="flex flex-col items-center mt-10 px-4">
      <HText>Cargo Management Dashboard</HText>

      <div className="flex flex-wrap justify-center gap-6 mt-6">
        {ACTIONS.map(({ label, icon }) => (
          <ActionCard
            key={label}
            icon={icon}
            label={label}
            onClick={() => setSelectedAction(label)}
          />
        ))}
      </div>

      <div className="w-full mt-10">{currentComponent}</div>
    </div>
  );
};

export default Management;
