import React, { useState, useEffect, useRef } from 'react';
import styles from './UniversalSearch.module.css';
// import styless from './testing.module.css';
import { BsRobot } from 'react-icons/bs';

const UniversalSearch: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [searchValue, setSearchValue] = useState('');
  const [chatMessages, setChatMessages] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const searchBarRef = useRef<HTMLDivElement | null>(null);
  // Retrieve userId, userName, and conversationId from localStorage or generate if not available
  const [userId, setUserId] = useState<string>(() => {
    const storedUserId = localStorage.getItem('userId');
    return storedUserId || generateRandomString(8);
  });

  const [userName, setUserName] = useState<string>(() => {
    const storedUserName = localStorage.getItem('userName');
    return storedUserName || generateRandomNumber(1000).toString();
  });

  const [conversationId, setConversationId] = useState<string>(() => {
    const storedConversationId = localStorage.getItem('conversationId');
    return storedConversationId || '';
  });

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

  useEffect(() => {
    // Retrieve userId and userName from localStorage or generate if not available
    const storedUserId = localStorage.getItem('userId');
    const userId = storedUserId || generateRandomString(8);
    const storedUserName = localStorage.getItem('userName');
    const userName = storedUserName || generateRandomNumber(1000).toString();

    // Store generated or retrieved values in localStorage
    localStorage.setItem('userId', userId);
    localStorage.setItem('userName', userName);

    // Check if conversationId is already set in localStorage, if not, generate it
    let conversationId: any = localStorage.getItem('conversationId');

    if (!conversationId) {
      // Create a new FormData object and append the user_id and name fields
      const formData = new FormData();
      formData.append('user_id', userId);
      formData.append('name', userName);

      // Make the initial API call to get conversation_id with form data
      fetch('https://tacklegpt.azurewebsites.net/api/answer/new_conversation', {
        method: 'POST',
        body: formData, // Use FormData as the body
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Failed to fetch user data from the API.');
          }
        })
        .then((data) => {
          // Store the conversation_id in localStorage
          localStorage.setItem('conversationId', data.id);
          conversationId = data.id;
        })
        .catch((error) => {
          console.error('An error occurred while fetching user data:', error);
        });
    }

    // Set userId, userName, and conversationId in state
    setUserId(userId);
    setUserName(userName);
    setConversationId(conversationId);
  }, []);

  const expandSearchBar = () => {
    setIsExpanded(true);
    // Welcome message when opening the chat
    if (chatMessages.length === 0) {
      setChatMessages([
        'Welcome to Tackle Company bot, what do you want to search for?',
      ]);
    }
  };

  const sendUserMessage = (message: string) => {
    const newChatMessages = [...chatMessages, message];
    setChatMessages(newChatMessages);

    // Retrieve userId and conversationId from localStorage
    const userId = localStorage.getItem('userId');
    const conversationId = localStorage.getItem('conversationId');

    if (!userId || !conversationId) {
      console.error('Missing user_id or conversationId in localStorage');
      return;
    }

    // Create a new FormData object and append the user_id, conversation_id, and question fields
    const formData_chat = new FormData();
    formData_chat.append('user_id', userId);
    formData_chat.append('conversation_id', conversationId);
    formData_chat.append('question', message);

    // Set isLoading to true to show the loader
    setIsLoading(true);

    fetch('https://tacklegpt.azurewebsites.net/api/answer/chat-docs', {
      method: 'POST',
      body: formData_chat,
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Failed to fetch answer from the API.');
        }
      })
      .then((data) => {
        // Get the answer from the API response
        const answer = data.answer;

        // Add the answer to the chat messages
        setChatMessages([...newChatMessages, answer]);
      })
      .catch((error) => {
        console.error('An error occurred while fetching the answer:', error);
      })
      .finally(() => {
        // Set isLoading to false after the API call is complete
        setIsLoading(false);
      });
  };

  // Function to generate a random string of a given length
  const generateRandomString = (length: number) => {
    const characters =
      'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += characters.charAt(
        Math.floor(Math.random() * characters.length)
      );
    }
    return result;
  };

  // Function to generate a random number within a specified range
  const generateRandomNumber = (max: number) => {
    return Math.floor(Math.random() * max) + 1;
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
          Hi ! <BsRobot className={styles.robotIcon} /> Welcome to Tackle
          Company Bot
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
