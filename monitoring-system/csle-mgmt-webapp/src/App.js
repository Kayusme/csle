import React from 'react';
import './App.css';
import MainContainer from "./components/MainContainer/MainContainer";
import NotFound from "./components/MainContainer/NotFound/NotFound";
import Emulations from "./components/MainContainer/Emulations/Emulations";
import Monitoring from "./components/MainContainer/Monitoring/Monitoring";
import Traces from "./components/MainContainer/Traces/Traces";
import EmulationStatistics from "./components/MainContainer/EmulationStatistics/EmulationStatistics";
import SystemModels from "./components/MainContainer/SystemModels/SystemModels";
import PolicyExamination from "./components/MainContainer/PolicyExamination/PolicyExamination";
import ContainerImages from "./components/MainContainer/ContainerImages/ContainerImages";
import Simulations from "./components/MainContainer/Simulations/Simulations";
import TrainingResults from "./components/MainContainer/TrainingResults/TrainingResults";
import About from "./components/MainContainer/About/About";
import Login from "./components/MainContainer/Login/Login";
import Policies from "./components/MainContainer/Policies/Policies";
import Jobs from "./components/MainContainer/Jobs/Jobs";
import SDNControllers from "./components/MainContainer/SDNControllers/SDNControllers";
import Downloads from "./components/MainContainer/Downloads/Downloads";
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import useSession from "./components/MainContainer/SessionManagement/useSession";
import { useAlert } from "react-alert";


function App() {
    const {sessionData, setSessionData} = useSession();
    const alert = useAlert();

    const ProtectedRoute = ({
                                user,
                                redirectPath = '/login-page',
                                children,
                            }) => {
        if (!sessionData) {
            alert.show("Only logged in users can access this page")
            return <Navigate to={redirectPath} replace/>;
        }
        return children;
    };

    return (
        <div className="App container-fluid">
            <div className="row">
                <div className="col-sm-12">
                    <BrowserRouter>
                        <Routes>
                            <Route path="/"
                                   element={<MainContainer/>}>
                                <Route index element={<Login setSessionData={setSessionData}
                                                             sessionData={sessionData}/>}>
                                </Route>
                                <Route path="emulations-page" index element={
                                    <ProtectedRoute>
                                        <Emulations sessionData={sessionData}/>
                                    </ProtectedRoute>}>
                                </Route>
                                <Route path="simulations-page" index element={
                                    <ProtectedRoute>
                                        <Simulations sessionData={sessionData}/>
                                    </ProtectedRoute>}>
                                </Route>
                                <Route path="monitoring-page" index element={
                                    <ProtectedRoute>
                                        <Monitoring sessionData={sessionData}/>
                                    </ProtectedRoute>}>
                                </Route>
                                <Route path="traces-page" index element={
                                    <ProtectedRoute>
                                        <Traces sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="emulation-statistics-page" index element={
                                    <ProtectedRoute>
                                        <EmulationStatistics sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="system-models-page" index element={
                                    <ProtectedRoute>
                                        <SystemModels sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="policy-examination-page" index element={
                                    <ProtectedRoute>
                                        <PolicyExamination sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="images-page" index element={
                                    <ProtectedRoute>
                                        <ContainerImages sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="training-page" index element={
                                    <ProtectedRoute>
                                        <TrainingResults sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="policies-page" index element={
                                    <ProtectedRoute>
                                        <Policies sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="jobs-page" index element={
                                    <ProtectedRoute>
                                        <Jobs sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="sdn-controllers-page" index element={
                                    <ProtectedRoute>
                                        <SDNControllers sessionData={sessionData}/>
                                    </ProtectedRoute>
                                }>
                                </Route>
                                <Route path="about-page" index element={<About/>}>
                                </Route>
                                <Route path="downloads-page" index element={<Downloads/>}>
                                </Route>
                                <Route path="login-page" index element={<Login setSessionData={setSessionData}
                                                                               sessionData={sessionData}/>}>
                                </Route>
                                <Route path="*" element={<NotFound/>}/>
                            </Route>
                        </Routes>
                    </BrowserRouter>
                </div>
            </div>
        </div>
    );
}

export default App;
