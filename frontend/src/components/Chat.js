import React, { useEffect, useState } from "react";
import {
    Box,
    Typography,
    Avatar,
    TextField,
    Button,
    Paper,
    Container,
    Grid,
    styled,
} from "@mui/material";
import { IoSendSharp } from "react-icons/io5";

const ChatContainer = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(2),
    borderRadius: theme.spacing(2),
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    background: "linear-gradient(#83C5BE, #EDF6F9, #83C5BE);",

// backgroundImage: "url('https://images.unsplash.com/photo-1557683311-eac922347aa1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1129&q=80')",
    backgroundSize: "cover",
    backgroundPosition: "center"
}));

const MessageBubble = styled(Box)(({ theme, isOutgoing }) => ({
    maxWidth: "70%",
    padding: theme.spacing(1, 2),
    borderRadius: theme.spacing(2),
    marginBottom: theme.spacing(1),
    backgroundColor: isOutgoing ? theme.palette.primary.main : theme.palette.background.paper,
    color: isOutgoing ? theme.palette.primary.contrastText : theme.palette.text.primary,
    alignSelf: isOutgoing ? "flex-end" : "flex-start",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
    transition: "all 0.3s ease-in-out",
    "&:hover": {
        transform: "translateY(-2px)",
        boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)"
    }
}));

export default function Chat({ setStarted, chatStyle, setChatStyle}) {
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [currentId, setCurrentId] = useState(1);
    const [messages, setMessages] = useState([
    ]);

    useEffect(() => {
        let objDiv = document.getElementById("chat");
        objDiv.scrollTop = objDiv.scrollHeight;
    }, [messages]);

    useEffect(() => {
        setIsLoading(true);
        fetch('http://localhost:5000/api/create_chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                org_id: 'maccabi',
                user_id: 'test_user',
                style: chatStyle === 'default' ? '' : chatStyle
            })
        }).then((res) => setIsLoading(false));
    }, [chatStyle])

    const handleSendMessage = () => {
        setStarted(true);
        setIsLoading(true);
        if (message.trim() === "") {
            setError("Message cannot be empty");
            return;
        }
        setError("");
        const newMessage = {
            id: currentId + 1,
            text: message,
            isOutgoing: true
        };
        const messagesUpdatedWithOutgoing = [...messages, newMessage];
        setMessages(messagesUpdatedWithOutgoing);

        fetch('http://localhost:5000/api/answer_question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: message
            })
        }).then(responseJson =>
            // TODO: check status before executing insertion
            responseJson.json().then(
                response => {
                    setMessages([...messagesUpdatedWithOutgoing, {
                        id: currentId + 2,
                        text: response.answer,
                        isOutgoing: false
                }]);
                setIsLoading(false);
                setCurrentId(currentId + 2);
            })
            );
        setMessage("");
    };

    return (
        <Container maxWidth="md">
            <ChatContainer elevation={2}>
                <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 2 }}>
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                        <Avatar
                            alt="John Doe"
                            src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
                            sx={{ width: 48, height: 48, mr: 2 }}
                        />
                        <Typography variant="h6">The Maccabi Expert</Typography>
                    </Box>
                </Box>


                <Box
                    sx={{
                        height: 400,
                        overflowY: "auto",
                        display: "flex",
                        flexDirection: "column",
                        mb: 2,
                        p: 2,
                        backgroundColor: "rgba(255, 255, 255, 0.8)",
                        borderRadius: 2
                    }}
                    id={'chat'}
                >
                    {messages.map((msg) => (
                        <MessageBubble key={msg.id} isOutgoing={msg.isOutgoing} style={msg.isOutgoing ? {backgroundColor: '#E29578'}: {}}>
                            <Typography variant="body1">{msg.text}</Typography>
                        </MessageBubble>
                    ))}
                </Box>

                <Grid container spacing={2} alignItems="flex-start">
                    <Grid item xs={12} sm={9}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="Type a message"
                            value={message}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    handleSendMessage();
                                }
                            }}
                            onChange={(e) => setMessage(e.target.value)}
                            error={!!error}
                            helperText={error}
                            InputProps={{
                                sx: { borderRadius: 4, backgroundColor: "white" }
                            }}
                        />
                    </Grid>
                    <Grid item xs={12} sm={3}>
                        <Button
                            fullWidth
                            variant="contained"
                            endIcon={<IoSendSharp />}
                            onClick={handleSendMessage}
                            sx={{ borderRadius: 4, height: "100%", backgroundColor: '#E29578' }}
                            disabled={isLoading}
                        >
                            Send
                        </Button>
                    </Grid>
                </Grid>
            </ChatContainer>
        </Container>
    );
};

