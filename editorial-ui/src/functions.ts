import { DocumentMetadata, DocumentEnrichments } from "models/document-model";


export function cleanText(text:string){
    // Remove underscores
    text = text.replace(/(_)/g, ' ');
    // Match starts with a letter or whitespace and letter, then capitalise
    return text.replace(/(^\w{1})|(\s+\w{1})/g, letter => letter.toUpperCase());
}

export function getMetaData(document_metadata:DocumentMetadata[]){
    var metadata:{documentName:string, docSourceURL:string, documentPublicationDate:string, classification:string, html: string} = {
        documentName: "",
        docSourceURL: "",
        documentPublicationDate: "",
        classification: "",
        html: "",
    }
    for (const metadata_obj of document_metadata){
        if(metadata_obj.name === "legislation_title"){
            metadata.documentName = metadata_obj.data;
        }
        if(metadata_obj.name === "legislation_identification"){
            metadata.docSourceURL = metadata_obj.data
        }
        if(metadata_obj.name === "legislation_enacted"){
            metadata.documentPublicationDate = metadata_obj.data;
        }
        if(metadata_obj.name === "legislation_classification" || metadata_obj.name === "orpml_classification"){
            metadata.classification = cleanText(metadata_obj.data);
            if((!metadata.classification) || (!metadata.classification.replace(/\s/g, '').length)){
                metadata.classification='No Classification'
            }
        }
        if(metadata_obj.name === "legislation_html"){
            metadata.html = metadata_obj.data;
        }
    }
    if(metadata.documentName === ""){
        metadata.documentName = 'No Title'
    }
    if(metadata.classification === ""){
        metadata.classification = 'No Classification'
    }
    if(metadata.documentPublicationDate === ""){
        metadata.documentPublicationDate = 'Unknown'
    }
    return metadata;
}

// Filter enrichments by type
export function filterEnrichmentsByDeonticLanguage(enrichments:any){
    if(enrichments.enrichment_def.name === 'deontic_language'){
        return enrichments
    }
}
export function filterEnrichmentsByNamedEntities(enrichments:any){
    if(enrichments.enrichment_def.name === 'named_entity_extraction'){
        return enrichments
    }
}

export function getEnrichmentsWithFeedback(document_enrichments:[DocumentEnrichments]|undefined){
    var feedbackCount = 0
    if(document_enrichments){
        for (const enrichments of document_enrichments){
            feedbackCount+=enrichments.enrichment_feedback.length
        }
    }
    return feedbackCount
}
