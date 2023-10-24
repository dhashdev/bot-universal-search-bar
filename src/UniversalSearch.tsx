import React, {useState, useEffect, useRef} from 'react';
import styles from './UniversalSearch.module.css';
// import styles from './testing.module.css';
import {BsRobot} from 'react-icons/bs';

const UniversalSearch: React.FC = () => {
    const [isExpanded, setIsExpanded] = useState(false);
    const [searchValue, setSearchValue] = useState('');
    const [chatMessages, setChatMessages] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const searchBarRef = useRef<HTMLDivElement | null>(null);

    const predefinedPrompts = [
        'What is this website about?',
        'What is the weather like today?',
        'I want to learn coding?',
    ];

    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (
                searchBarRef.current &&
                !searchBarRef.current.contains(e.target as Node)
            ) {
                setIsExpanded(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const expandSearchBar = () => {
        setIsExpanded(true);
        // Welcome message when opening the chat
        if (chatMessages.length === 0) {
            setChatMessages([
                'Welcome to dhashdev bot, what do you want to search for?',
            ]);
        }
    };

    const sendUserMessage = async (message: string) => {
        const newChatMessages = [...chatMessages, message];
        setChatMessages(newChatMessages);

        // Send a request to the FastAPI backend
        setIsLoading(true);

        const response = await fetch('http://localhost:8000/get-response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({message: message})
        });

        const data = await response.json();
        const apiResponse = data.response;

        setIsLoading(false);
        setChatMessages([...newChatMessages, apiResponse]);
    };

    const handlePredefinedPromptClick = (prompt: string) => {
        // Treat predefined prompts as user messages and send them
        sendUserMessage(prompt);
    };

    return (
        <div
            className={`${styles['universal-search']} ${
                isExpanded ? styles.expanded : ''
            }`}
            ref={searchBarRef}
        >
            <div className={`${styles.prompts} ${isExpanded ? styles.visible : ''}`}>
                <div className={styles.botHeader}>
                    Hi ! <BsRobot className={styles.robotIcon}/> Welcome to Dhash Bot
                </div>

                {chatMessages.map((message, index) => (
                    <div
                        key={index}
                        className={`${
                            index % 2 === 0
                                ? styles['chat-message-left']
                                : styles['chat-message-right']
                        }`}
                    >
                        {message}
                    </div>
                ))}

                {/* {predefinedPrompts.map((prompt, index) => (
          <div
            key={index}
            className={styles.predefinedPrompt}
            onClick={() => handlePredefinedPromptClick(prompt)}
          >
            {prompt}
          </div>
        ))} */}

                {isLoading && (
                    <div className={styles['chat-message-left']}>
                        <div className={styles['loading-dots']}>
                            <div className={styles['dot']}></div>
                            <div className={styles['dot']}></div>
                            <div className={styles['dot']}></div>
                        </div>
                    </div>
                )}
            </div>
            <input
                type='text'
                placeholder='What can I help you with?'
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onClick={expandSearchBar}
                onKeyDown={(e) => {
                    if (e.key === 'Enter' && searchValue.trim() !== '') {
                        // Send user message and clear the input
                        sendUserMessage(searchValue);
                        setSearchValue('');
                    }
                }}
            />
        </div>
    );
};

export default UniversalSearch;
