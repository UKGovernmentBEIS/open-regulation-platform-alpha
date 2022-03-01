import React, { useState }from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Link,
  Redirect,
  Route,
  RouteProps,
  Switch,
} from "react-router-dom";
import { DocumentsPage } from "components/DocumentListPage";
import { DocumentPage } from "components/DocumentReviewPage";
import { LoginForm } from "components/LoginForm";
import { Main, TopNav } from "govuk-react";
import jwtDecode from "jwt-decode";
import { Button } from "@mui/material";
import LogoutIcon from '@mui/icons-material/Logout';


interface JWT {
  exp: number;
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>();

  function logout(){
    localStorage.removeItem('jwt');
    setIsAuthenticated(false);
  }
  const HeaderBtn = (
    <TopNav.Anchor as={Link} to={"/login"}><Button onClick={()=>logout()} style={{backgroundColor:"#001F38", color:"white", padding: "10px 20px"}}><LogoutIcon sx={{marginRight: 1}}/>Log Out</Button></TopNav.Anchor>
  );

  const CompanyLink = (
    <TopNav.Anchor as={Link} to={"/documents"}>Open Regulation Platform</TopNav.Anchor>
  );

  function LandingPage() {
    let cookie = localStorage.getItem('jwt');
    if(cookie){
      let decoded: JWT = jwtDecode(cookie);
      const now = new Date().getTime();
      if (now > (decoded.exp* 1000)) {
        logout();
        return <Redirect to="/login" />;
      }
      else{
        setIsAuthenticated(true);
        return <Redirect to="/documents" />;
      }
    }
    else{
      logout();
      return <Redirect to="/login" />;
    }
  }

  function AuthenticatedRoute({ children, ...rest }: RouteProps) {
    if (!isAuthenticated) {
      return <Redirect to="/" />;
    }

    return <Route {...rest}>{children}</Route>;
  }

  return (
    <Router>
      <React.Fragment>
        <div className="App">
          <TopNav company={CompanyLink} style={{paddingTop:10, paddingBottom:10}} serviceTitle={isAuthenticated? HeaderBtn : ""}></TopNav>
          <Main>
            <Switch>
              <Route exact path="/">
                <LandingPage />
              </Route>
              <Route exact path="/login">
                <LoginForm setIsAuthenticated={setIsAuthenticated}/>
              </Route>
              <AuthenticatedRoute exact path="/documents">
                <DocumentsPage />
              </AuthenticatedRoute>
              <AuthenticatedRoute path="/documents/:documentId">
                <DocumentPage />
              </AuthenticatedRoute>
            </Switch>
          </Main>
        </div>
      </React.Fragment>
    </Router>
  );
}

export default App;
