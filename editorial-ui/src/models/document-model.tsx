interface EnrichmentDefinition {
    name: string;
}

export interface DocumentEnrichments {
    id: number;
    data: string;
    enrichment_def: EnrichmentDefinition;
    enrichment_feedback: [{
        good: boolean;
        notes: string;
        user_id: number;
    }];
    extent: {
        sections: [{
            extent_char_end: number | undefined;
            extent_char_start: number | undefined;
            extent_end: string | null;
            extent_start: string | null;
        }]
    };
}

interface DocumentType {
    id: number;
    name: string;
}

export interface DocumentMetadata {
    data: string;
    name: string;
    document_metadata_definition_id: string
}

export interface Document {
    document_id: string;
    document_type: DocumentType;
    document_metadata: DocumentMetadata[];
    document_enrichments: [DocumentEnrichments];
    raw_text?: string;
  }