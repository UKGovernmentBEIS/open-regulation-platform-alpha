import React from "react";
import { useHistory  } from "react-router-dom";
import { Table } from "govuk-react";
import { Document } from "../models/document-model";
import { getMetaData, getEnrichmentsWithFeedback } from "../functions";
import EnrichmentPopover from "./EnrichmentPopover";

interface DocumentRowProps {
    orpDocument: Document;
}
const DocumentRow: React.FC<DocumentRowProps> = ({orpDocument}) => {
    const authority = orpDocument.document_type.name;
    const metadata = getMetaData(orpDocument.document_metadata);

    const totalEnrichments = orpDocument.document_enrichments.length;
    const enrichmentsWithFeedback = getEnrichmentsWithFeedback(orpDocument.document_enrichments)

    const getProgressBG = (completedEnrichments: number, totalEnrichments:number) => {
        if(completedEnrichments===totalEnrichments){
            return (<><span className={`progress-circle bg-green`}></span><span>Completed</span></>)
        }
        else if(completedEnrichments === 0){
            return (<><span className={`progress-circle bg-gray`}></span><span>Not Started</span></>)
        }
        else if(completedEnrichments < totalEnrichments){
            return (<><span className={`progress-circle bg-blue`}></span><span>In Progress</span></>)
        }
        else{
            return (<><span className={`progress-circle bg-red`}></span><span>Error</span></>)
        }
    }
    const history = useHistory();
    const handleRowClick = () => {
        history.push(`/documents/${orpDocument.document_id}`);
    }

    return (
        <React.Fragment>
            <tr onClick={() => handleRowClick()} style={{cursor:"pointer"}}>
                <Table.Cell>
                    <p><b>{metadata.classification}</b></p>
                    <p>{metadata.documentName}</p>
                </Table.Cell>
                <Table.Cell>
                    <EnrichmentPopover enrichmentsWithFeedback={enrichmentsWithFeedback} totalEnrichments={totalEnrichments} enrichments={orpDocument.document_enrichments}></EnrichmentPopover>
                </Table.Cell>
                <Table.Cell><p>{authority}</p></Table.Cell>
                <Table.Cell><p>{metadata.documentPublicationDate}</p></Table.Cell>
                <Table.Cell><p style={{display:"flex"}}>{getProgressBG(enrichmentsWithFeedback, totalEnrichments)}</p></Table.Cell>
            </tr>
        </React.Fragment>
    )
}

export default DocumentRow