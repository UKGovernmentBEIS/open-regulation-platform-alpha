// First Party
import React from "react";

// Third Party
import { GridRow, Button, H4, Select } from "govuk-react";
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';

// Project
import Services from "../services";
import { Document, DocumentEnrichments } from "../models/document-model";

const btnMargin = [{size: 3, direction: ['left', 'right']}, { size: 2, direction: ['top', 'bottom'] }]
const modalTitleTextStyle={ color: 'white', textAlign: "center" }

interface ModalProps {
    orpDocument: Document;
    setDocument: (values:Document) => void;
    modalState: boolean;
    setModalState: (values: boolean) => void;
    modalNotesState: boolean;
    setNotesModalState: (values:boolean) => void;
    activeEnrichmentTask: DocumentEnrichments,
}
export const FeedbackModal: React.FC<ModalProps> = ({
    orpDocument, setDocument, modalState, setModalState, modalNotesState, setNotesModalState, activeEnrichmentTask
}) => {

    // Submit positive or negative feedback via the modal
    function submitEnrichmentFeedback(activeEnrichmentTask:DocumentEnrichments | undefined, good: boolean, notes: string){
        if(activeEnrichmentTask){
            Services.submitFeedbackToEndpoint(activeEnrichmentTask.id, good, notes).then(() => {
                Services.getDocument(orpDocument.document_id).then((response) => {
                    setDocument(response.data[0] as Document);
                });
            });
        }
        if(good){
            setModalState(false)
        }
        else{
            setNotesModalState(false)
        }
    }

    // Get the review question to be displayed on the modal
    function getReviewQuestion(activeEnrichmentTask:DocumentEnrichments | undefined){
        if(activeEnrichmentTask)
        {
            if(activeEnrichmentTask.enrichment_def.name==="deontic_language"){
                return "Are the highlighted words the correct obligation?"
            }
            else if(activeEnrichmentTask.enrichment_def.name==="named_entity_extraction"){
                return "Is this a named entity?"
            }
        }
        else{return ""}
    }

    return (
        <React.Fragment>
            <Modal
                open={modalState}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
                hideBackdrop={true}
                disableScrollLock
                style={{ position: 'initial' }}
                disableAutoFocus={true}
                disableEnforceFocus={true}
            >
                <Box sx={{
                    position: 'absolute',
                    top: '45%',
                    left: '70%',
                    transform: 'translate(0%, 130%)',
                    width: 400,
                    bgcolor: '#17334A',
                    border: '2px solid #000',
                    boxShadow: 20,
                    p: 4,
                }}>
                    {modalNotesState?
                        <>
                            <H4 style={modalTitleTextStyle}>What is wrong with the highlighted obligation?</H4>
                            <Select input={{
                                name: 'Please Select',
                                onChange: (args:any) => {
                                    const optionIndex = args.target.options.selectedIndex
                                    const optionValue = args.target.options[optionIndex].innerText
                                    submitEnrichmentFeedback(activeEnrichmentTask, false, optionValue)
                                    setModalState(false)
                                }
                            }}
                            style={{width:"200%"}}>
                                <option value="0">
                                    Please Select...
                                </option>
                                <option value="1">
                                    Incorrect text is higlighted
                                </option>
                                <option value="2">
                                    The highlighted text is of a different enrichment type
                                </option>
                                <option value="3">
                                    No text is highlighted
                                </option>
                            </Select>
                        </>
                        :
                        <>
                            <H4 style={modalTitleTextStyle}>
                                { getReviewQuestion(activeEnrichmentTask) }
                            </H4>
                            <GridRow className="modalBtnsRow">
                                <Button onClick={() => submitEnrichmentFeedback(activeEnrichmentTask, true, "")} margin={btnMargin} className="modalBtn">Yes</Button>
                                <Button onClick={() => setNotesModalState(true)} margin={btnMargin} className="modalBtn" buttonColour="red">No</Button>
                            </GridRow>
                        </>
                    }
                </Box>
            </Modal>
        </React.Fragment>
    )
}