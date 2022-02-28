// First Party
import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import { useHistory } from "react-router-dom";

// Third Party
import { GridRow, GridCol, Table, BackLink, Button, H3, H4, Caption, ButtonArrow } from "govuk-react";
import DOMPurify from "dompurify";

// Project
import Services from "../services";
import { getMetaData, getEnrichmentsWithFeedback, filterEnrichmentsByDeonticLanguage, filterEnrichmentsByNamedEntities } from "../functions";
import { EnrichmentTaskList } from "./EnrichmentTaskList";
import { FeedbackModal } from "./FeedbackModal";
import { Document, DocumentEnrichments } from "../models/document-model";

const btnMargin = [{size: 3, direction: ['left', 'right']}, { size: 2, direction: ['top', 'bottom'] }];
const arrowStyles = {backgroundColor:"#001F38", color:"white", padding: "15px 15px", borderRadius:"25px", height:"50px", width: "135%"};
const upArrow = Object.assign(arrowStyles, {marginBottom:"5px", marginTop:"15px"});
const downArrow = Object.assign(arrowStyles, {marginBottom:"20px", marginTop:"20px"});

export const DocumentPage: React.FC = () => {
    // Get document ID passed through url
    const { documentId } = useParams<{documentId: string}>();

    // Back Button
    const history = useHistory();
    const routeChange = () =>{
        let path = `/documents`;
        history.push(path);
    }

    // Request the document through the API and set the first enrichment to be the current active one
    let [orpDocument, setDocument] = useState<Document>();
    let [activeEnrichmentTask, setActiveEnrichmentTask] = useState<DocumentEnrichments>();
    useEffect(() => {
        Services.getDocument(documentId).then((response) => {
            setDocument(response.data[0] as Document);
            setActiveEnrichmentTask(response.data[0].document_enrichments[0] as DocumentEnrichments);
        });
    }, [documentId]);

    const metadata = getMetaData(orpDocument?orpDocument.document_metadata:[])

    // Every time the active enrichment is updated, update the HTML entity markers
    let [akn2html, setAkn2html] = useState<HTMLElement>(document.createElement('document'))
    let [entityCounter, setEntityCounter] = useState<number>(1)
    useEffect(() => {
        if(activeEnrichmentTask){
            if(activeEnrichmentTask.extent.sections[0].extent_start){
                var documenthtml = document.createElement('document');
                documenthtml.innerHTML = metadata.html
                var counter:number = 0
                // Loop over all the extents for a particular enrichment task
                for (const extent of activeEnrichmentTask.extent.sections){
                    if(extent.extent_start){
                        counter = counter+1
                        // Use xPath and the HTML extents to find the relevant text
                        var extent_start = extent.extent_start.replace('body', '/')
                        var result = document.evaluate(extent_start, documenthtml, null, XPathResult.ANY_TYPE, null );
                        var element = result.iterateNext() as Element

                        // Highlight the text
                        if(element){
                            const markStart = `<mark id='scrollToHere${counter}'>`;
                            const markEnd = "</mark>";
                            if(extent.extent_char_start!=null && extent.extent_char_end!=null){
                                // Insert the start of the <mark> html
                                element.innerHTML= [
                                    element.innerHTML.slice(0, extent.extent_char_start),
                                    markStart,
                                    element.innerHTML.slice(extent.extent_char_start)
                                ].join('');
                                // Insert the end of the <mark> html
                                element.innerHTML= [
                                    element.innerHTML.slice(0, extent.extent_char_end+markStart.length),
                                    markEnd,
                                    element.innerHTML.slice(extent.extent_char_end+markStart.length)
                                ].join('');
                            }
                            else{
                                element.innerHTML= markStart+element.innerHTML+markEnd
                            }
                        }
                    }
                }
                // Update the HTML
                setAkn2html(documenthtml)
            }
        }
    }, [activeEnrichmentTask, metadata.html]);

    // Submit positive or negative feedback via the modal
    const [modalState, setModalState] = React.useState(true);
    const [modalNotesState, setNotesModalState] = React.useState(false);

    // Get list of enrichments by type
    var deonticLanguageTasks:DocumentEnrichments[] | undefined = [];
    var namedEntityTasks:DocumentEnrichments[] | undefined = [];
    if(orpDocument){
        deonticLanguageTasks = orpDocument.document_enrichments.filter(filterEnrichmentsByDeonticLanguage);
        namedEntityTasks = orpDocument.document_enrichments.filter(filterEnrichmentsByNamedEntities);
    }

    const totalEnrichmentsWithFeedback= getEnrichmentsWithFeedback(orpDocument?.document_enrichments)

    // Feedback must be given on all enrichment tasks before document can be submitted
    function submitAllFeedback(){
        if(orpDocument){
            Services.submitAllDocumentFeedback(orpDocument.document_id).then(() => {
                history.push('/documents')
            }).catch(function (error) {
                if (error.response) {
                  // Request made and server responded
                  alert(error.response.data.message);
                }
                else {
                  // The request was made but no response was received
                  alert(error.message);
                }
            });
        }
    }

    // Cycle through ehighlighted extents
    let [disablePrevEntity, setDisablePrevEntity] = useState<boolean>(true)
    let [disableNextEntity, setDisableNextEntity] = useState<boolean>(false)
    function prevEntity(){
        var counter = entityCounter-1;
        var scrollElement = document.getElementById(`scrollToHere${counter}`);
        if(scrollElement){
            setDisableNextEntity(false)
            setEntityCounter(entityCounter-1);
            counter = counter -1;
            scrollElement = document.getElementById(`scrollToHere${counter}`);
            if(!scrollElement){
                setDisablePrevEntity(true)
            }
        }
    }
    function nextEntity(){
        var counter = entityCounter+1;
        var scrollElement = document.getElementById(`scrollToHere${counter}`);
        if(scrollElement){
            setDisablePrevEntity(false)
            setEntityCounter(entityCounter+1);
            counter = counter +1;
            scrollElement = document.getElementById(`scrollToHere${counter}`);
            if(!scrollElement){
                setDisableNextEntity(true);
            }
        }
    }

    // Every time the HTML is updated, scroll to the highlighted text
    useEffect(() => {
        var scrollElement = document.getElementById(`scrollToHere${entityCounter}`);
        if(scrollElement){
            scrollElement.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
            if(entityCounter === 1){
                setDisableNextEntity(true);
            }
        }
        var nextScrollElement = document.getElementById(`scrollToHere${entityCounter+1}`);
        if(nextScrollElement){
            setDisableNextEntity(false);
        }
    }, [akn2html, entityCounter]);

    return (
        <React.Fragment>
            <GridRow>
                <GridCol setWidth="one-half">
                    <div id="enrichmentCol">
                        <BackLink onClick={routeChange} style={{cursor:"pointer"}}>Back to my tasks</BackLink>
                        <H3>{metadata.classification}</H3>
                        <H4>{metadata.documentName}</H4>
                        <Button style={{backgroundColor:"#738492", color:"white", padding: "15px 25px", borderRadius:"30px"}} onClick={() => window.open(metadata.docSourceURL, "_blank")}>Visit Document Source</Button>
                        <div className="enrichment-list">
                            {orpDocument ?
                                <Table id="document-table">
                                    {deonticLanguageTasks.length?
                                    <Table.Row>
                                        <Table.Cell>
                                            <EnrichmentTaskList key={activeEnrichmentTask?activeEnrichmentTask.id:0}
                                                enrichmentTasks={deonticLanguageTasks}
                                                activeEnrichmentTask={activeEnrichmentTask}
                                                setState={setModalState}
                                                setNotesModalState={setNotesModalState}
                                                setActiveEnrichmentTask={setActiveEnrichmentTask}
                                                setEntityCounter={setEntityCounter}>
                                            </EnrichmentTaskList>
                                        </Table.Cell>
                                    </Table.Row>
                                    :<></>}
                                    {namedEntityTasks.length?
                                    <Table.Row>
                                        <Table.Cell>
                                            <EnrichmentTaskList key={activeEnrichmentTask?activeEnrichmentTask.id:0}
                                                enrichmentTasks={namedEntityTasks}
                                                activeEnrichmentTask={activeEnrichmentTask}
                                                setState={setModalState}
                                                setNotesModalState={setNotesModalState}
                                                setActiveEnrichmentTask={setActiveEnrichmentTask}
                                                setEntityCounter={setEntityCounter}>
                                            </EnrichmentTaskList>
                                        </Table.Cell>
                                    </Table.Row>
                                    :<></>}
                                </Table>
                            : undefined }
                            <Button disabled={totalEnrichmentsWithFeedback!==orpDocument?.document_enrichments.length} onClick={()=>submitAllFeedback()} icon={<ButtonArrow />} buttonColour={"#007ACD"} buttonHoverColour={"black"} padding={btnMargin}>Submit Document</Button>
                        </div>
                    </div>
                </GridCol>
                <div id="feedbackBtns">
                    <Button disabled={disablePrevEntity} onClick={() => prevEntity()} style={upArrow}>↑</Button>
                    <Caption size="M">{entityCounter}/{activeEnrichmentTask?.extent.sections.length}</Caption >
                    <Button disabled={disableNextEntity} onClick={() => nextEntity()} style={downArrow}>↓</Button>
                </div>
                <GridCol id="review-column" setWidth="one-half">
                    <div>
                        <div id="review-editor" dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(akn2html)}}></div>
                    </div>
                </GridCol>
                <GridRow>
                    {
                        orpDocument ? activeEnrichmentTask ?
                            <FeedbackModal
                                orpDocument={orpDocument}
                                setDocument={setDocument}
                                modalState={modalState}
                                setModalState={setModalState}
                                modalNotesState={modalNotesState}
                                setNotesModalState={setNotesModalState}
                                activeEnrichmentTask={activeEnrichmentTask}
                            ></FeedbackModal>
                            :<></>
                        :<></>
                    }
                </GridRow>
            </GridRow>
        </React.Fragment>
    )
}