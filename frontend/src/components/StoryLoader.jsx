import {useState,useEffect} from 'react'
import { useParams, useNavigate } from 'react-router-dom';
import axios from "axios";
import LoadingStatus from './LoadingStatus';
import StoryGame from './StoryGame';

const API_BASE_URL="/api"



const StoryLoader = () => {
        const {id}=useParams();
        const navigate=useNavigate();
        const [story,setStory]=useState(null)
        const [loading,setLoading]=useState(true)
        const [error,setError]=useState(null)

        useEffect(()=>{
                LoadStory();
        },[id])

        const LoadStory=async (storyId)=>{
                setLoading(true)
                setError(null)
                try{
                        const response=await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`)
                        setStory(response.data)
                }catch(err){
                      if(err.response?.status==404){
                        setError("Story Not Found.")
                      } else{
                        setError("Faild to Load Story")
                      } 
                }finally{
                        setLoading(false)
                }
        }
        const createNewStory=()=>{
                navigate("/")
        }
        if(loading){
                return <LoadingStatus theme={"Story"} />
        }
        if(error) {
                return <div>
                        <div>
                                <h2>Story not Found</h2>
                                {error}
                                <button onClick={createNewStory}>Go To Story Generator</button>
                        </div>
                </div>
        }
        if(story){
                return <div>
                        <StoryGame story={story} onNewStory={createNewStory} />
                </div>
        }
}

export default StoryLoader
