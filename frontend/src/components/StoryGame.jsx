import { useState,useEffect } from "react";


const StoryGame = ({story,onNewStory}) => {
        const [currentNodeId,setCurrentNodeId]=useState(null);
        const [currentNode,setCurrentNode]=useState(null);
        const [options,setOptions]=useState([])
        const [isEnding,setIsEnding]=useState(false)
        const [isWinningEnding,setIsWinningEnding]=useState(false)

        useEffect(()=>{
                if(story && story.root_node ){
                        const rootNodeId=story.root_node.id;
                        setCurrentNodeId(rootNodeId)
                }
        },[story])
        useEffect(()=>{
                if(currentNodeId && story && story.all_nodes){
                        const node=story.all_nodes[currentNodeId];
                        setCurrentNode(node);
                        setIsEnding(node.is_ending)
                        setIsWinningEnding(node.is_winning_ending)
                        if(!node.is_ending && node.options && node.options.length>0){
                                setOptions(node.setOptions)
                        }else{
                                setOptions([])
                        }
                }
        },[currentNodeId,story])
        const chooseOption=(optionId)=>{
                setCurrentNode(optionId)
        }
        const restartStory=()=>{
                if(story && story.root_node){
                        setCurrentNodeId(story.root_node.id)
                }
        }
  return (
    <div className="flex">
        <header>
                <h2>{story.title}</h2>
        </header>
        <div className="flex">
                {currentNode && <div className="flex">
                        <p>{currentNode.content}</p>
                        {isEnding ? <div>
                                <h3>{isWinningEnding?"Congratulations":"The End"}</h3>
                                {isWinningEnding?"You reached a winning Ending":"Your adventure has ended"}
                        </div>:
                        <div className="flex">
                                <h3>What will you do? </h3>
                                <div className="">
                                        {options.map((option,index)=>(
                                                <button key={index}
                                                onClick={chooseOption(option.node_id)}
                                                className="bg-slate-500 text-white"
                                                >
                                                        {option.text}
                                                </button>
                                        ))}
                                </div>
                        </div>}
                </div>}
                <div>
                        <button onClick={restartStory}>Restart Story</button>
                </div>
                {onNewStory && <button onClick={onNewStory} className="bg-blue-600 text-white">New Story</button>}
        </div>
    </div>
  )
}

export default StoryGame
