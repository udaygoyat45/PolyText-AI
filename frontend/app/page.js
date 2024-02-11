'use client';

import Image from "next/image";
import { useState, useEffect, useDebugValue } from 'react';
import styles from './FileUploader.module.css';

export default function Home() {
  const [medias, setMedias] = useState([]);
  const [chatLogs, setChatLogs] = useState([]);
  const [uploadError, setUploadError] = useState(null);
  const [message, setMessage] = useState('');
  const [threadId, setThreadId] = useState();
  const [waiting, setWaiting] = useState(false);

  useEffect(() => {
    
    
    const fillMedia = async () => {
      const listResponse = await fetch(`http://localhost:4000/media/list/`);
      const all_medias = await listResponse.json();
      setMedias(all_medias.medias);
    }

    const fillLogs = async () => {
      const threads = await fetch(`http://localhost:4000/chatbot/list`);
      const allThreads = await threads.json();
      const thread_one = allThreads.threads[0];
      setThreadId(thread_one);

      const listLogs = await fetch(`http://localhost:4000/chatbot/list_messages/${thread_one}`);
      const allLogs = await listLogs.json();
      console.log(allLogs)
      setChatLogs(allLogs.messages);
    }

    fillLogs();
    fillMedia();
  }, []);

  const handleFileChange = async (event) => {
    let fileType = event.target.files[0].type.replace('/', '-');
    console.log('file type:', fileType);

    if (fileType === "") {
      setUploadError("This media type isn't supported yet. Read About Page to see supported media types.")
      return;
    }

    const supportedResponse = await fetch(`http://localhost:4000/media/check/${fileType}`);
    const supportedResponseData = await supportedResponse.json();

    if (supportedResponseData.media_supported) {
      setUploadError(null);
      const formData = new FormData();
      formData.append("file", event.target.files[0]);

      const uploadResponse = await fetch(`http://localhost:4000/media/upload/`, {
        method: 'POST',
        body: formData,
      });

      const uploadData = await uploadResponse.json();

      if ('success' in uploadData) {
        const newMedia = uploadData.new_media;
        setMedias([...medias, newMedia]);
      } else {
        setUploadError("This media type isn't supported yet. Read About Page to see supported media types.")
      }
    } else {
      setUploadError("This media type isn't supported yet. Read About Page to see supported media types.")
    }

  }

  const handleSendMessage = async () => {
    setChatLogs(chatLogs => [...chatLogs, {'role': 'user', 'content': message}])
    setWaiting(true);

    const newQuery = await fetch(`http://localhost:4000/chatbot/new_message/`, {
      method: 'POST',
      body: JSON.stringify({thread_id: threadId, message: message}),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const queryAnswer = await newQuery.json();
    setChatLogs(chatLogs => [...chatLogs, {'role': 'assistant', 'content': queryAnswer.reply}])
    setWaiting(false);
  }

  return (
    <div className="flex" style={{height: '86vh'}}>
      <div className="m-2 w-1/3 p-6 bg-zinc-100 rounded-lg">

        <label htmlFor="fileInput" className="mb-4">
          {uploadError ? <div className="mb-5 text-red-900">{uploadError}</div> : <div></div>}
          <input type="file" id="fileInput" onChange={handleFileChange} className="hidden" />
          <div className="flex items-center justify-center w-full h-12 bg-blue-500 text-white rounded-md cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Upload File
          </div>
        </label>

        {medias.length > 0 ? (
          medias.map((media, index) => (
            <div key={index} className="mt-4">
              <p className="font-semibold">Name: {media.name}</p>
              <p>Type: {media.type}</p>
            </div>
          ))
        )
          : <div className="flex justify-center mt-5"> Press upload to start adding learning points for PolyText AI!</div>}
      </div>


      <div className="mt-2 mr-2 mb-2 w-2/3 p-6 rounded-lg">
        <h2 className="flex text-2xl font-semibold mb-4 justify-center">Chatbar</h2>
        <div className="flex flex-col h-full justify-between">
          <div className="flex overflow-y-auto flex-col-reverse">
            {waiting ? <span className="font-bold m-5 flex justify-center">Generating response...</span> : <div></div>}
            {chatLogs.length > 0 ?
              chatLogs.slice(0).reverse().map((log, index) => (
                <div key={index} className="mt-3 ml-5 mr-10">
                  {log.role == 'user' ? 
                    <h1 className="font-bold">User</h1>
                  :  <h1 className="font-bold">Assistant</h1>
                  }
                  {log.content}
                  {index == 0 && <div className="mb-40"></div>}
                </div>
              ))
              : <div>Type something to get started</div>}

          </div>

          <div className="flex justify-between items-center mb-8">
            <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} className="w-full py-2 px-4 border rounded-lg mr-2" placeholder="Ask PolyText AI anything..." />
            <button onClick={handleSendMessage} className="bg-blue-500 text-white py-2 px-4 rounded-full hover:bg-blue-600">Send</button>
          </div>
        </div>
      </div>

    </div>
  )
}
