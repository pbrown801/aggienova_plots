import React from "react";
import { usePlotSettings } from "../../contexts/PlotSettingsContext";
import { useSelectedSNe } from "../../contexts/SelectedSNeContext";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import type { YAxisType } from "../../contexts/PlotSettingsContext";

interface YAxisToggleComponentProps {
  onNoData: (message: string) => void;
}

const YAxisToggleComponent: React.FC<YAxisToggleComponentProps> = ({ onNoData }) => {
  const { yAxisType, setYAxisType } = usePlotSettings();
  const { selectedSNe, setSelectedSNe } = useSelectedSNe();

  const handleChange = (
    event: React.MouseEvent<HTMLElement>,
    newYAxisType: YAxisType | null
  ) => {
    if (newYAxisType !== null) {
      if (newYAxisType === "absolute") {
        const filteredSNe = selectedSNe.filter((sn) => sn.distance_modulus !== null);
        const removedSNe = selectedSNe.filter((sn) => sn.distance_modulus === null);

        if (removedSNe.length > 0) {
          const snNames = removedSNe.map((sn) => sn.sn_name).join(", ");
          onNoData(`The following supernovae have been removed due to missing distance modulus: ${snNames}`);
        }

        setSelectedSNe(filteredSNe);
      }
      setYAxisType(newYAxisType);
    }
  };

  return (
    <ToggleButtonGroup
      value={yAxisType}
      exclusive
      onChange={handleChange}
      aria-label="y-axis type"
    >
      <ToggleButton value="apparent" aria-label="apparent">
        Apparent
      </ToggleButton>
      <ToggleButton value="absolute" aria-label="absolute">
        Absolute
      </ToggleButton>
      <ToggleButton value="diff_max" aria-label="diff_max">
        Diff Max
      </ToggleButton>
    </ToggleButtonGroup>
  );
};

export default YAxisToggleComponent;