import {Box, Button, Typography} from "@mui/material";
import Chat from "./Chat";
import React, {useState} from "react";
import './ChatManager.css'

export default function ChatManager() {
    const [started, setStarted] = useState(false);
    const [chatStyle, setChatStyle] = useState('');

    // TODO: on chat style replace, get the history of current style?


    return (
        <Box sx={{
            height: '100%',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            gap: '25px'
        }}>
            <Typography variant={'h1'}  style={{color: '#006D77', marginTop: '10px', fontFamily: 'Cookie'}}>
                MoodiBot
            </Typography>
            <Chat
                setStarted={setStarted}
                chatStyle={chatStyle}
                setChatStyle={setChatStyle}
            />

            {!started && <div style={{display: "flex", alignItems: "center"}}>
                <Typography variant={'h4'} style={{fontFamily: 'Cookie'}}>
                    What's your mood?
                </Typography>
                <div>
                    {['default', 'rhymes', 'kids', 'elderly', 'emoji'].map(element =>
                        <Button
                            key={element}
                            style={{color: "black", backgroundColor: "#83C5BE", borderRadius: "5px", marginLeft: "2px"}}
                            onClick={() => {
                                setStarted(true);
                                setChatStyle(element);
                            }}>
                            {element}
                        </Button>
                    )}
                </div>
            </div>}
        </Box>
    )
}