import React, { useEffect, useState } from "react";
import { GridRow, GridCol, Table, H3, H2 } from "govuk-react";
import Services from "../services";
import DocumentRow from "./DocumentRow";
import { Document } from "../models/document-model";
import { UserInfo } from "../models/user-model";


export const DocumentsPage: React.FC = () => {
  let [documents, setDocuments] = useState<Document[]>([]);
  let [userInfo, setInfo] = useState<UserInfo>({
    id: 0,
    first_name: "Unnamend",
    last_name: "User",
    email: ""
  });

  useEffect(() => {
    Services.docsWithEnrichments().then((response) => {
      setDocuments(response.data as Document[]);
    });
  }, []);

  useEffect(() => {
    Services.getUserInfo().then((response) => {
      setInfo(response.data[0])
    });
  }, []);

  const documentList = (): JSX.Element[] => {
    return documents.map((doc) => {
      return (
        <DocumentRow key={doc.document_id} orpDocument={doc}/>
      )
    })
  }

  return (
    <React.Fragment>
      <GridRow>
        <GridCol><H3>{userInfo.first_name + ' ' + userInfo.last_name}</H3></GridCol>
      </GridRow>
      <GridRow>
        <GridCol><H2>Outstanding Documents</H2></GridCol>
      </GridRow>
      <Table id="document-table" head={
        <Table.Row>
          <Table.CellHeader><h4>Task Title</h4></Table.CellHeader>
          <Table.CellHeader><h4>Enrichments</h4></Table.CellHeader>
          <Table.CellHeader><h4>Authority</h4></Table.CellHeader>
          <Table.CellHeader><h4>Publication Date</h4></Table.CellHeader>
          <Table.CellHeader><h4>Status</h4></Table.CellHeader>
        </Table.Row>
      }>
        {documents ? (documentList()) : null}
      </Table>
    </React.Fragment>
  );
}
