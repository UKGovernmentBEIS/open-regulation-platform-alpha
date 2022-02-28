import { useState } from "react";
import { useHistory } from "react-router-dom";

import { Button, FormGroup, Label, Input, ErrorText, Heading, Paragraph, ButtonArrow } from "govuk-react";

import Services from "services";


interface IProps {
    setIsAuthenticated: (values:boolean) => void;
}
export const LoginForm:React.FC<IProps> = ({setIsAuthenticated}) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const history = useHistory();

    function validateForm() {
        return email.length > 0 && password.length > 0;
    }

    function handleSubmit(event: { preventDefault: () => void; }) {
        event.preventDefault();
        setIsAuthenticated(false)
        localStorage.setItem('jwt', '');
        Services.login(email, password).then((response) => {
            if(response.status === 200){
                localStorage.setItem('jwt', response.data['signed_jwt']);
                setIsAuthenticated(true)
                history.push('/');
            }
        }).catch(function (error) {
            if (error.response) {
              // Request made and server responded
              setError(error.response.data.message);
            } else{
              // The request was made but no response was received
              setError(error.message);
            }
        });
    }

    return (
    <div className="Login">
        <form onSubmit={handleSubmit}>
            <Heading size="LARGE">
                Log In
            </Heading>
            <Paragraph>
                Log into your account with the password we previously sent you.
            </Paragraph>
            <FormGroup >
                <Label style={{marginTop: "30px"}}>Email</Label>
                <Input
                    required
                    autoFocus
                    type="email"
                    value={email}
                    onChange={(e:any) => setEmail(e.target.value)}
                />
            </FormGroup>
            <FormGroup >
                <Label>Password</Label>
                <Input
                    required
                    type="password"
                    value={password}
                    onChange={(e:any) => setPassword(e.target.value)}
                />
            </FormGroup>
            <Button start icon={<ButtonArrow/>} type="submit" disabled={!validateForm()} buttonColour="#1d70b8">
                Log In
            </Button>
            {error? <ErrorText>{error}</ErrorText>:<></>}
        </form>
    </div>
    );
}
