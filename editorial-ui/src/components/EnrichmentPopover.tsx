import React from "react";
import { DocumentEnrichments } from "../models/document-model";
import { cleanText, filterEnrichmentsByNamedEntities, filterEnrichmentsByDeonticLanguage } from "../functions";
import { FaInfoCircle } from "react-icons/fa";
import Popover from '@mui/material/Popover';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

interface PopoverProps {
    enrichmentsWithFeedback: number,
    totalEnrichments: number,
    enrichments: DocumentEnrichments[],
}
const EnrichmentPopover: React.FC<PopoverProps> = ({enrichmentsWithFeedback, totalEnrichments, enrichments}) => {

    var deonticLanguageTasks:DocumentEnrichments[] | undefined = enrichments.filter(filterEnrichmentsByDeonticLanguage)
    var namedEntityTasks:DocumentEnrichments[] | undefined = enrichments.filter(filterEnrichmentsByNamedEntities)

    // Enrichment Popover
    const [anchorEl, setAnchorEl] = React.useState(null);
    const handlePopoverOpen = (event:any) => {
      setAnchorEl(event.currentTarget);
    };
    const handlePopoverClose = () => {
      setAnchorEl(null);
    };
    const open = Boolean(anchorEl);

    return (
        <React.Fragment>
            <p>
                {enrichmentsWithFeedback}/{totalEnrichments}
                    <FaInfoCircle
                        aria-owns={open ? 'mouse-over-popover' : undefined}
                        aria-haspopup="true"
                        onMouseEnter={handlePopoverOpen}
                        onMouseLeave={handlePopoverClose}
                        style={{marginLeft:"20px"}}>
                    </FaInfoCircle>
                <Popover
                    id="mouse-over-popover"
                    sx={{
                        pointerEvents: 'none',
                    }}
                    open={open}
                    anchorEl={anchorEl}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'center',
                    }}
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'center',
                    }}
                    PaperProps={{
                        style: {
                            backgroundColor: "transparent",
                            boxShadow: "none",
                            borderRadius: 16
                        }
                    }}
                    onClose={handlePopoverClose}
                    disableRestoreFocus
                >
                    <Box
                    sx={{
                        position: "relative",
                        mt: "20px",
                        "&::before": {
                            backgroundColor: "#001F38",
                            content: '""',
                            display: "block",
                            position: "absolute",
                            width: 24,
                            height: 24,
                            top: -10,
                            transform: "rotate(45deg)",
                            left: "calc(50% - 12px)",
                        }
                    }}
                    />
                    <div id="enichmentPopover">
                        <Typography sx={{ p: 1 }}><b style={{marginRight: 5}}>{deonticLanguageTasks.length}</b> {deonticLanguageTasks[0]?cleanText(deonticLanguageTasks[0].enrichment_def.name):"Deontic Language"}</Typography>
                        <Typography sx={{ p: 1 }}><b style={{marginRight: 5}}>{namedEntityTasks.length}</b> {namedEntityTasks[0]?cleanText(namedEntityTasks[0].enrichment_def.name):"Named Entity"}</Typography>
                    </div>
                </Popover>
            </p>
        </React.Fragment>
    )
}

export default EnrichmentPopover