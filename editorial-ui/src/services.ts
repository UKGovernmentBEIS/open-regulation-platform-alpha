import qs from 'qs';
import API from './api';

const bearer = 'Bearer '
const Services = {
    login: (email: string, password: string) => {
        return API.post('/rpc/login', {
            email: email,
            password: password,
        }, {
            headers: { Authorization: null }
        });
    },
    getUserInfo: () => {
        return API.get('/user_info', {
            headers: {
                Authorization:  bearer + localStorage.getItem('jwt'),
                'Content-Type': 'application/json',
            }
        });
    },
    docsWithEnrichments: () => {
        const params = qs.stringify({
            select: 'document_id:id,document_type(id,name),document_metadata:document_metadata_view(data,name),document_enrichments:enrichment(id,enrichment_def(name),enrichment_feedback(good,notes,user_id))'
        });

        return API.get(`/docs_with_outstanding_feedback?${params}`, {
            headers: {
                Authorization:  bearer + localStorage.getItem('jwt'),
                'Content-Type': 'application/json',
                'Range-Unit': 'items',
                Range: '0-14',
            }
        });
    },
    getDocument: (documentId:string) => {
        const params = qs.stringify({
            select: `document_id:id,document_type(id,name),raw_text,related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_info(first_name,last_name,email))))
            &id=eq.${documentId}
            &document_metadata_view.category=in.(title,enacted,identification,classification,html)`
        },{ encode: false });

        return API.get(`/document?${params}`, {
            headers: {
                Authorization:  bearer + localStorage.getItem('jwt'),
                'Content-Type': 'application/json',
            }
        });
    },
    submitFeedbackToEndpoint: (enrichmentId:number, good: boolean, notes: string) => {
        var data = {
            "enrichment_id": enrichmentId,
            "good": good,
            "notes": notes,
        }
        return API.post(`/enrichment_feedback`, data, {
            headers: {
                Authorization:  bearer + localStorage.getItem('jwt'),
                'Content-Type': 'application/json',
            }
        });
    },
    submitAllDocumentFeedback: (documentId:string) => {
        var data = {
            "document_id": documentId,
            "feedback_status" : "review_complete"
        }
        return API.post(`/document_enrichment_feedback_status`, data, {
            headers: {
                Authorization:  bearer + localStorage.getItem('jwt'),
                'Content-Type': 'application/json',
            }
        });
    },
}

export default Services;