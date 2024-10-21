import React, { useState } from "react";
import {
    Box,
    Typography,
    Avatar,
    IconButton,
    TextField,
    Button,
    Paper,
    Container,
    Grid,
    styled
} from "@mui/material";
import { IoCallOutline, IoVideocamOutline, IoSendSharp } from "react-icons/io5";

const ChatContainer = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(2),
    borderRadius: theme.spacing(2),
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    backgroundImage: "url('https://images.unsplash.com/photo-1557683311-eac922347aa1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1129&q=80')",
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

export default function Chat() {
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [messages, setMessages] = useState([
        { id: 1, text: "Hello!", isOutgoing: false },
        { id: 2, text: "Hi there! How are you?", isOutgoing: true },
        { id: 3, text: "I'm doing great, thanks for asking!", isOutgoing: false }
    ]);

    const handleSendMessage = () => {
        if (message.trim() === "") {
            setError("Message cannot be empty");
            return;
        }
        setError("");
        const newMessage = {
            id: messages.length + 1,
            text: message,
            isOutgoing: true
        };
        setMessages([...messages, newMessage]);
        setMessage("");
    };

    return (
        <Container maxWidth="md">
            <ChatContainer elevation={3}>
                <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 2 }}>
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                        <Avatar
                            alt="John Doe"
                            src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
                            sx={{ width: 48, height: 48, mr: 2 }}
                        />
                        <Typography variant="h6">John Doe</Typography>
                    </Box>
                    <Box>
                        <IconButton aria-label="Voice call">
                            <IoCallOutline />
                        </IconButton>
                        <IconButton aria-label="Video call">
                            <IoVideocamOutline />
                        </IconButton>
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
                >
                    {messages.map((msg) => (
                        <MessageBubble key={msg.id} isOutgoing={msg.isOutgoing}>
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
                            color="primary"
                            endIcon={<IoSendSharp />}
                            onClick={handleSendMessage}
                            sx={{ borderRadius: 4, height: "100%" }}
                        >
                            Send
                        </Button>
                    </Grid>
                </Grid>
            </ChatContainer>
        </Container>
    );
};

