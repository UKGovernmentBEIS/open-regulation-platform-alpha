import React from "react";
import { GridRow, GridCol } from "govuk-react";
import { DocumentEnrichments } from "../models/document-model";
import { FaInfoCircle } from "react-icons/fa";
import { cleanText } from "functions";

const enrichmentMargin = [{size: 3, direction: ['left', 'right']}, { size: 1, direction: ['top'] }]
var goodFeedbackTaskStyles = {
    cursor:"pointer",
    backgroundColor: "green",
    color: "white",
}
var badFeedbackTaskStyles = {
    cursor:"pointer",
    backgroundColor: "red",
    color: "white",
}
var activeTaskStyles = {
    cursor:"pointer",
    backgroundColor: "#17334A",
    color: "white",
}
var taskStyles = {
    cursor:"pointer",
    backgroundColor: "white",
    color: "black",
}

interface DocumentEnrichmentProps {
    enrichmentTasks: DocumentEnrichments[];
    setState: (values:boolean) => void;
    setNotesModalState: (values:boolean) => void;
    setActiveEnrichmentTask: (activeEnrichmentTask: DocumentEnrichments) => void;
    activeEnrichmentTask: DocumentEnrichments | undefined;
    setEntityCounter: (values:number) => void;
}
export const EnrichmentTaskList: React.FC<DocumentEnrichmentProps> = ({
    enrichmentTasks, setState, setNotesModalState, activeEnrichmentTask, setActiveEnrichmentTask, setEntityCounter}) => {
    function getTaskStyles(currentEnrichment:DocumentEnrichments, activeEnrichment:DocumentEnrichments|undefined){
        if(currentEnrichment.id===(activeEnrichment?activeEnrichment.id:0)){
            return activeTaskStyles
        }
        if(currentEnrichment.enrichment_feedback[currentEnrichment.enrichment_feedback.length-1]){
            return currentEnrichment.enrichment_feedback[currentEnrichment.enrichment_feedback.length-1].good ? goodFeedbackTaskStyles: badFeedbackTaskStyles
        }
        else{
            return taskStyles
        }
    }

    function onTaskClick(task:DocumentEnrichments){
        setActiveEnrichmentTask(task);
        setNotesModalState(false);
        setState(true);
        setEntityCounter(1);
    }

    return (
        <React.Fragment>
            <GridRow margin={1}>
                <GridCol>
                    {enrichmentTasks[0] ? <p>{cleanText(enrichmentTasks[0].enrichment_def.name)} <FaInfoCircle style={{float:"right"}}></FaInfoCircle></p>: null}
                </GridCol>
            </GridRow>
                {enrichmentTasks ? (
                    <>
                        {enrichmentTasks.map((task) => (
                            <GridRow style={getTaskStyles(task, activeEnrichmentTask)} onClick={() => onTaskClick(task)} margin={enrichmentMargin} className="enrichment">
                                <GridCol setWidth="one-fifth"><p><b>{task.id}</b></p></GridCol>
                                <GridCol><p>Enrichment Title</p></GridCol>
                            </GridRow>
                        ))}
                    </>
                ) : null}
        </React.Fragment>
    )
}