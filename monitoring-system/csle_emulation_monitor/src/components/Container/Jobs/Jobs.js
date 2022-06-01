import React, {useState, useCallback, useEffect, createRef} from 'react';
import './Jobs.css';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner';
import Accordion from 'react-bootstrap/Accordion';
import TrainingJob from "./TrainingJob/TrainingJob";
import DataCollectionJob from "./DataCollectionJob/DataCollectionJob";
import SystemIdentificationJob from "./SystemIdentificationJob/SystemIdentificationJob";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import Select from 'react-select'
import { useDebouncedCallback } from 'use-debounce';

const Jobs = () => {
    const [showTrainingJobsInfoModal, setShowTrainingJobsInfoModal] = useState(false);
    const [trainingJobsLoading, setTrainingJobsLoading] = useState(false);
    const [trainingJobs, setTrainingJobs] = useState([]);
    const [trainingJobsIds, setTrainingJobsIds] = useState([]);
    const [selectedTrainingJobId, setSelectedTrainingJobId] = useState(null);
    const [selectedTrainingJob, setSelectedTrainingJob] = useState(null);
    const [loadingSelectedTrainingJob, setLoadingSelectedTrainingJob] = useState(true);
    const [filteredTrainingJobsIds, setFilteredTrainingJobsIds] = useState([]);
    const [showDataCollectionJobsInfoModal, setShowDataCollectionJobsInfoModal] = useState(false);
    const [dataCollectionJobsLoading, setDataCollectionJobsLoading] = useState(false);
    const [dataCollectionJobs, setDataCollectionJobs] = useState([]);
    const [dataCollectionJobsIds, setDataCollectionJobsIds] = useState([]);
    const [selectedDataCollectionJobId, setSelectedDataCollectionJobId] = useState(null);
    const [selectedDataCollectionJob, setSelectedDataCollectionJob] = useState(null);
    const [loadingSelectedDataCollectionJob, setLoadingSelectedDataCollectionJob] = useState(true);
    const [showOnlyRunningTrainingJobs, setShowOnlyRunningTrainingJobs] = useState(false);
    const [filteredDataCollectionJobsIds, setFilteredDataCollectionJobsIds] = useState([]);
    const [showOnlyRunningDataCollectionJobs, setShowOnlyRunningDataCollectionJobs] = useState(false);
    const [trainingJobsSearchString, setTrainingJobsSearchString] = useState("");
    const [dataCollectionJobsSearchString, setDataCollectionJobsSearchString] = useState("");
    const [showSystemIdentificationJobsInfoModal, setShowSystemIdentificationJobsInfoModal] = useState(false);
    const [systemIdentificationJobsLoading, setSystemIdentificationJobsLoading] = useState(false);
    const [systemIdentificationJobs, setSystemIdentificationJobs] = useState([]);
    const [systemIdentificationJobsIds, setSystemIdentificationJobsIds] = useState([]);
    const [selectedSystemIdentificationJobId, setSelectedSystemIdentificationJobId] = useState(null);
    const [selectedSystemIdentificationJob, setSelectedSystemIdentificationJob] = useState(null);
    const [loadingSelectedSystemIdentificationJob, setLoadingSelectedSystemIdentificationJob] = useState(true);
    const [systemIdentificationJobsSearchString, setSystemIdentificationJobsSearchString] = useState("");
    const [filteredSystemIdentificationJobsIds, setFilteredSystemIdentificationJobsIds] = useState([]);
    const [showOnlyRunningSystemIdentificationJobs, setShowOnlyRunningSystemIdentificationJobs] = useState(false);

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const fetchTrainingJobs = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/trainingjobs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setTrainingJobs(response);
                setFilteredTrainingJobsIds(response);
                setTrainingJobsLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchTrainingJobsIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/trainingjobsids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const trainingJobsIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", simulation: " + id_obj.simulation + ", emulation: " + id_obj.emulation
                    }
                })
                setTrainingJobsIds(trainingJobsIds)
                setFilteredTrainingJobsIds(trainingJobsIds)
                setTrainingJobsLoading(false)
                if (trainingJobsIds.length > 0) {
                    setSelectedTrainingJobId(trainingJobsIds[0])
                    fetchTrainingJob(trainingJobsIds[0])
                    setLoadingSelectedTrainingJob(true)
                } else {
                    setLoadingSelectedTrainingJob(false)
                    setSelectedTrainingJob(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchDataCollectionJobs = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setDataCollectionJobs(response);
                setFilteredDataCollectionJobsIds(response);
                setDataCollectionJobsLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchDataCollectionJobIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobsids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const dataCollectionJobIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", emulation: " + id_obj.emulation
                    }
                })
                setDataCollectionJobsIds(dataCollectionJobIds)
                setFilteredDataCollectionJobsIds(dataCollectionJobIds)
                setDataCollectionJobsLoading(false)
                if (dataCollectionJobIds.length > 0) {
                    setSelectedDataCollectionJobId(dataCollectionJobIds[0])
                    fetchDataCollectionJob(dataCollectionJobIds[0])
                    setLoadingSelectedDataCollectionJob(true)
                } else {
                    setLoadingSelectedDataCollectionJob(false)
                    setSelectedDataCollectionJob(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSystemIdentificationJobs = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSystemIdentificationJobs(response);
                setFilteredSystemIdentificationJobsIds(response);
                setSystemIdentificationJobsLoading(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSystemIdentificationJobsIds = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobsids',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const systemIdentificationJobsIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: "ID: " + id_obj.id + ", emulation: " + id_obj.emulation
                    }
                })
                setSystemIdentificationJobsIds(systemIdentificationJobsIds)
                setFilteredSystemIdentificationJobsIds(systemIdentificationJobsIds)
                setSystemIdentificationJobsLoading(false)
                if (systemIdentificationJobsIds.length > 0) {
                    setSelectedSystemIdentificationJobId(systemIdentificationJobsIds[0])
                    fetchSystemIdentificationJob(systemIdentificationJobsIds[0])
                    setLoadingSelectedSystemIdentificationJob(true)
                } else {
                    setLoadingSelectedSystemIdentificationJob(false)
                    setSelectedSystemIdentificationJob(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setTrainingJobsLoading(true)
        fetchTrainingJobsIds()
        setDataCollectionJobsLoading(true)
        fetchDataCollectionJobIds()
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobsIds()
    }, [fetchTrainingJobsIds, fetchDataCollectionJobIds, fetchSystemIdentificationJobsIds]);

    const removeTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/remove/' + training_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllTrainingJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        removeTrainingJobRequest(job.id)
    }

    const removeAllTrainingJobs = () => {
        setTrainingJobsLoading(true)
        removeAllTrainingJobsRequest()
    }

    const removeSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/remove/' + system_identification_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllSystemIdentificationJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        removeSystemIdentificationJobRequest(job.id)
    }

    const removeAllSystemIdentificationJobs = () => {
        setSystemIdentificationJobsLoading(true)
        removeAllSystemIdentificationJobsRequest()
    }

    const stopTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/stop/' + training_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setTrainingJobsLoading(true)
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchTrainingJob = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/get/' + training_job_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedTrainingJob(response)
                setLoadingSelectedTrainingJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        stopTrainingJobRequest(job.id)
    }

    const stopSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/stop/' + system_identification_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchSystemIdentificationJob = useCallback((system_identification_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/get/' + system_identification_job_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedSystemIdentificationJob(response)
                setLoadingSelectedSystemIdentificationJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        stopSystemIdentificationJobRequest(job.id)
    }

    const startTrainingJobRequest = useCallback((training_job_id) => {
        fetch(
            `http://` + ip + ':7777/trainingjobs/start/' + training_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setTrainingJobsLoading()
                fetchTrainingJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startTrainingJob = (job) => {
        setTrainingJobsLoading(true)
        startTrainingJobRequest(job.id)
    }

    const startSystemIdentificationJobRequest = useCallback((system_identification_job_id) => {
        fetch(
            `http://` + ip + ':7777/systemidentificationjobs/start/' + system_identification_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSystemIdentificationJobsLoading(true)
                fetchSystemIdentificationJobsIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startSystemIdentificationJob = (job) => {
        setSystemIdentificationJobsLoading(true)
        startSystemIdentificationJobRequest(job.id)
    }

    const trainingJobSearchFilter = (job_id_obj, searchVal) => {
        return (searchVal === "" || job_id_obj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1);
    }

    const systemIdentificationJobSearchFilter = (job_id_obj, searchVal) => {
        return (searchVal === "" || job_id_obj.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1);
    }

    const searchTrainingJobChange = (event) => {
        var searchVal = event.target.value
        const filteredTJobIds = trainingJobsIds.filter(job => {
            return trainingJobSearchFilter(job, searchVal)
        });
        setFilteredTrainingJobsIds(filteredTJobIds)
        setTrainingJobsSearchString(trainingJobsSearchString)

        var selectedTrainingJobRemoved = false
        if(!loadingSelectedTrainingJob && filteredTJobIds.length > 0){
            for (let i = 0; i < filteredTJobIds.length; i++) {
                if(selectedTrainingJob !== null && selectedTrainingJob !== undefined &&
                    selectedTrainingJob.id === filteredTJobIds[i].value) {
                    selectedTrainingJobRemoved = true
                }
            }
            if(!selectedTrainingJobRemoved) {
                setSelectedTrainingJobId(filteredTJobIds[0])
                fetchTrainingJob(filteredTJobIds[0])
                setLoadingSelectedTrainingJob(true)
            }
        }
    }

    const searchSystemIdentificationJobChange = (event) => {
        var searchVal = event.target.value
        const filteredSIJobsIds = systemIdentificationJobsIds.filter(job => {
            return systemIdentificationJobSearchFilter(job, searchVal)
        });
        setFilteredSystemIdentificationJobsIds(filteredSIJobsIds)
        setSystemIdentificationJobsSearchString(systemIdentificationJobsSearchString)

        var selectedSystemIdentificationJobRemoved = false
        if(!loadingSelectedSystemIdentificationJob && filteredSIJobsIds.length > 0){
            for (let i = 0; i < filteredSIJobsIds.length; i++) {
                if(selectedSystemIdentificationJob !== null && selectedSystemIdentificationJob !== undefined &&
                    selectedSystemIdentificationJob.id === filteredSIJobsIds[i].value) {
                    selectedSystemIdentificationJobRemoved = true
                }
            }
            if(!selectedSystemIdentificationJobRemoved) {
                setSelectedSystemIdentificationJobId(filteredSIJobsIds[0])
                fetchSystemIdentificationJob(filteredSIJobsIds[0])
                setLoadingSelectedSystemIdentificationJob(true)
            }
        }
    }

    const runningTrainingJobsChange = (event) => {
        if(!showOnlyRunningTrainingJobs) {
            const filteredTrainJobs = filteredTrainingJobsIds.filter(job => {
                return job.running
            });
            setFilteredTrainingJobsIds(filteredTrainJobs)
        } else {
            const filteredTrainJobs = trainingJobs.filter(job => {
                return trainingJobSearchFilter(job, trainingJobsSearchString)
            });
            setFilteredTrainingJobsIds(filteredTrainJobs)
        }
        setShowOnlyRunningTrainingJobs(!showOnlyRunningTrainingJobs)
    }

    const runningDataCollectionJobsChange = (event) => {
        if (!showOnlyRunningDataCollectionJobs) {
            const filteredDataCollectionJobs = filteredDataCollectionJobs.filter(job => {
                return job.running
            });
            setFilteredDataCollectionJobsIds(filteredDataCollectionJobs)
        } else {
            const filteredDataCollectionJobs = dataCollectionJobs.filter(job => {
                return dataCollectionJobSearchFilter(job, dataCollectionJobsSearchString)
            });
            setFilteredDataCollectionJobsIds(filteredDataCollectionJobs)
        }
        setShowOnlyRunningDataCollectionJobs(!showOnlyRunningDataCollectionJobs)
    }

    const runningSystemIdentificationJobsChange = (event) => {
        if(!showOnlyRunningSystemIdentificationJobs) {
            const filteredSystemIdentificationJobs = filteredSystemIdentificationJobs.filter(job => {
                return job.running
            });
            setFilteredSystemIdentificationJobsIds(filteredSystemIdentificationJobs)
        } else {
            const filteredSystemIdentificationJobs = systemIdentificationJobs.filter(job => {
                return systemIdentificationJobSearchFilter(job, systemIdentificationJobsSearchString)
            });
            setFilteredSystemIdentificationJobsIds(filteredSystemIdentificationJobs)
        }
        setShowOnlyRunningSystemIdentificationJobs(!showOnlyRunningSystemIdentificationJobs)
    }

    const searchTrainingJobHandler = useDebouncedCallback(
        (event) => {
            searchTrainingJobChange(event)
        },
        350
    );

    const searchSystemIdentificationJobHandler = useDebouncedCallback(
        (event) => {
            searchSystemIdentificationJobChange(event)
        },
        350
    );

    const dataCollectionJobSearchFilter = (job_id, searchVal) => {
        return (searchVal === "" || job_id.label.toLowerCase().indexOf(searchVal.toLowerCase()) !== -1);
    }

    const searchDataCollectionJobChange = (event) => {
        var searchVal = event.target.value
        const filteredDCJobsIds = dataCollectionJobsIds.filter(job_id => {
            return dataCollectionJobSearchFilter(job_id, searchVal)
        });
        setFilteredDataCollectionJobsIds(filteredDCJobsIds)
        setDataCollectionJobsSearchString(searchVal)

        var selectedDataCollectionJobRemoved = false
        if(!loadingSelectedDataCollectionJob && filteredDCJobsIds.length > 0){
            for (let i = 0; i < filteredDCJobsIds.length; i++) {
                if(selectedDataCollectionJob !== null && selectedDataCollectionJob !== undefined &&
                    selectedDataCollectionJob.id === filteredDCJobsIds[i].value) {
                    selectedDataCollectionJobRemoved = true
                }
            }
            if(!selectedDataCollectionJobRemoved) {
                setSelectedDataCollectionJobId(filteredDCJobsIds[0])
                fetchDataCollectionJob(filteredDCJobsIds[0])
                setLoadingSelectedDataCollectionJob(true)
            }
        }
    }

    const searchDataCollectionJobHandler = useDebouncedCallback(
        (event) => {
            searchDataCollectionJobChange(event)
        },
        350
    );

    const removeDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/remove/' + data_collection_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setDataCollectionJobsLoading(true)
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeAllDataCollectionJobsRequest = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/remove',
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setDataCollectionJobsLoading()
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        removeDataCollectionJobRequest(job.id)
    }

    const removeAllDataCollectionJobs = (job) => {
        setDataCollectionJobsLoading(true)
        removeAllDataCollectionJobsRequest()
    }

    const stopDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/stop/' + data_collection_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setDataCollectionJobsLoading()
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const fetchDataCollectionJob = useCallback((data_collection_job_id) => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/get/' + data_collection_job_id.value,
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setSelectedDataCollectionJob(response)
                setLoadingSelectedDataCollectionJob(false)
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const stopDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        stopDataCollectionJobRequest(job.id)
    }

    const startDataCollectionJobRequest = useCallback((data_collection_job_id) => {
        fetch(
            `http://` + ip + ':7777/datacollectionjobs/start/' + data_collection_job_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                setDataCollectionJobsLoading(true)
                fetchDataCollectionJobIds()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const startDataCollectionJob = (job) => {
        setDataCollectionJobsLoading(true)
        startDataCollectionJobRequest(job.id)
    }

    const refreshTrainingJobs = () => {
        setTrainingJobsLoading(true)
        fetchTrainingJobsIds()
    }

    const refreshSystemidentificationJobs = () => {
        setSystemIdentificationJobsLoading(true)
        fetchSystemIdentificationJobsIds()
    }

    const refreshDataCollectionJobs = () => {
        setDataCollectionJobsLoading(true)
        fetchDataCollectionJobIds()
    }

    const renderTrainingJobsInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the training jobs
        </Tooltip>
    );

    const renderRemoveAllTrainingJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all training jobs.
        </Tooltip>
    );

    const renderRemoveAllDataCollectionJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all data collection jobs.
        </Tooltip>
    );

    const renderRefreshTrainingJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload training jobs from the backend
        </Tooltip>
    );

    const renderDataCollectionJobsInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the data collection jobs
        </Tooltip>
    );

    const renderRefreshDataCollectionJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload data collection jobs from the backend
        </Tooltip>
    );

    const renderSystemIdentificationJobsInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the system identification jobs
        </Tooltip>
    );

    const renderRemoveAllSystemIdentificationJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove all system identification jobs.
        </Tooltip>
    );

    const renderRefreshSystemIdentificationJobsTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload system identification jobs from the backend
        </Tooltip>
    );

    const updateSelectedTrainingJobId = (selectedId) => {
        setSelectedTrainingJobId(selectedId)
        fetchTrainingJob(selectedId)
        setLoadingSelectedTrainingJob(true)
    }

    const updateSelectedDataCollectionJobId = (selectedId) => {
        setSelectedDataCollectionJobId(selectedId)
        fetchDataCollectionJob(selectedId)
        setLoadingSelectedDataCollectionJob(true)
    }

    const updateSelectedSystemIdentificationJob = (selectedId) => {
        setSelectedSystemIdentificationJobId(selectedId)
        fetchSystemIdentificationJob(selectedId)
        setLoadingSelectedSystemIdentificationJob(true)
    }

    const SelectTrainingJobOrSpinner = (props) => {
        if (!props.trainingJobsLoading && props.trainingJobsIds.length === 0) {
            return (
                <span className="emptyText">No training jobs are available</span>
            )
        }
        if (props.trainingJobsLoading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching training jobs... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Training job:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedTrainingJobId}
                                defaultValue={props.selectedTrainingJobId}
                                options={props.trainingJobsIds}
                                onChange={updateSelectedTrainingJobId}
                                placeholder="Select job"
                            />
                        </div>
                    </div>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTrainingJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshTrainingJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderTrainingJobsInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowTrainingJobsInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <TrainingJobsInfoModal show={showTrainingJobsInfoModal}
                                           onHide={() => setShowTrainingJobsInfoModal(false)}/>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveAllTrainingJobsTooltip}
                    >
                        <Button variant="danger" onClick={removeAllTrainingJobs}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
    }


    const SelectDataCollectionJobOrSpinner = (props) => {
        if (!props.dataCollectionJobsLoading && props.dataCollectionJobsIds.length === 0) {
            return (
                <span className="emptyText">No data collection jobs are available</span>
            )
        }
        if (props.dataCollectionJobsLoading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching data collection jobs... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Data collection job:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedDataCollectionJobId}
                                defaultValue={props.selectedDataCollectionJobId}
                                options={props.dataCollectionJobsIds}
                                onChange={updateSelectedDataCollectionJobId}
                                placeholder="Select job"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshDataCollectionJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshDataCollectionJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderDataCollectionJobsInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowDataCollectionJobsInfoModal(true)}
                                className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <DataCollectionJobsInfoModal show={showDataCollectionJobsInfoModal}
                                                 onHide={() => setShowDataCollectionJobsInfoModal(false)}/>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveAllDataCollectionJobsTooltip}
                    >
                        <Button variant="danger" onClick={removeAllDataCollectionJobs}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
    }

    const SelectSystemIdentificationJobOrSpinner = (props) => {
        if (!props.systemIdentificationJobsLoading && props.systemIdentificationJobsIds.length === 0) {
            return (
                <span className="emptyText">No system identification jobs are available</span>
            )
        }
        if (props.systemIdentificationJobsLoading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching system identification jobs... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
        } else {
            return (
                <div className="inline-block">
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            System identification job:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "600px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedSystemIdentificationJobId}
                                defaultValue={props.selectedSystemIdentificationJobId}
                                options={props.systemIdentificationJobsIds}
                                onChange={updateSelectedSystemIdentificationJob}
                                placeholder="Select job"
                            />
                        </div>
                    </div>
                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshSystemIdentificationJobsTooltip}
                    >
                        <Button variant="button" onClick={refreshSystemidentificationJobs}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderSystemIdentificationJobsInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowSystemIdentificationJobsInfoModal(true)} className="infoButton2">
                            <i className="fa fa-info-circle" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                    <SystemIdentificationJobsInfoModal show={showSystemIdentificationJobsInfoModal}
                                                       onHide={() => setShowSystemIdentificationJobsInfoModal(false)}/>

                    <OverlayTrigger
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveAllSystemIdentificationJobsTooltip}
                    >
                        <Button variant="danger" onClick={removeAllSystemIdentificationJobs}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
    }

    const TrainingJobsInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Training jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Training jobs</h4>
                    <p className="modalText">
                        A training job represents an ongoing execution of training policies.
                        The list of training jobs enables real-time monitoring of jobs.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const SystemIdentificationJobsInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        System identification jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>System identification jobs</h4>
                    <p className="modalText">
                        A system identification job represents an ongoing process for estimating a system model
                        for an emulation.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const DataCollectionJobsInfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Data Collection Jobs
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Data Collection jobs</h4>
                    <p className="modalText">
                        A data collection job represents an ongoing execution of data collection.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const wrapper = createRef();

    const TrainingJobAccordion = (props) => {
        if (props.loadingSelectedTrainingJob || props.selectedTrainingJob === null || props.selectedTrainingJob === undefined) {
            if(props.loadingSelectedTrainingJob) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching selected training job... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    <TrainingJob job={props.selectedTrainingJob} wrapper={wrapper} key={props.selectedTrainingJob.id}
                                 removeTrainingJob={removeTrainingJob} stopTrainingJob={stopTrainingJob}
                                 startTrainingJob={startTrainingJob}/>
                </Accordion>
            )
        }
    }

    const SystemIdentificationJobAccordion = (props) => {
        if (props.loadingSelectedSystemIdentificationJob || props.selectedSystemIdentificationJob === null
            || props.selectedSystemIdentificationJob === undefined) {
            if(props.loadingSelectedSystemIdentificationJob) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching selected system identification job... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>)
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    <SystemIdentificationJob job={props.selectedSystemIdentificationJob} wrapper={wrapper}
                                             key={props.selectedSystemIdentificationJob.id}
                                             removeSystemIdentificationJob={removeSystemIdentificationJob}
                                             stopSystemIdentificationJob={stopSystemIdentificationJob}
                                             startSystemIdentificationJob={startSystemIdentificationJob}/>
                </Accordion>
            )
        }
    }

    const DataCollectionJobAccordion = (props) => {
        if (props.loadingSelectedDataCollectionJob || props.selectedDataCollectionJob === null ||
            props.selectedDataCollectionJob === undefined) {
            if(props.loadingSelectedDataCollectionJob) {
                return (
                    <h3>
                        <span className="spinnerLabel"> Fetching selected data collection job... </span>
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden"></span>
                        </Spinner>
                    </h3>
                )
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <Accordion defaultActiveKey="0">
                    <DataCollectionJob job={props.selectedDataCollectionJob} wrapper={wrapper} key={props.selectedDataCollectionJob.id}
                                       removeDataCollectionJob={removeDataCollectionJob}
                                       stopDataCollectionJob={stopDataCollectionJob}
                                       startDataCollectionJob={startDataCollectionJob}
                    />
                </Accordion>
            )
        }
    }

    return (
        <div className="policyExamination">
            <div className="row">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectTrainingJobOrSpinner trainingJobsLoading={trainingJobsLoading}
                                                   trainingJobsIds={filteredTrainingJobsIds}
                                                   selectedTrainingJobId={selectedTrainingJobId}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="trainingJobInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="trainingJobInput"
                                onChange={searchTrainingJobHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>

            <TrainingJobAccordion loadingSelectedTrainingJob={loadingSelectedTrainingJob}
                                    selectedTrainingJob={selectedTrainingJob}/>


            <div className="row systemIdentificationJobs">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectDataCollectionJobOrSpinner dataCollectionJobsLoading={dataCollectionJobsLoading}
                                                          dataCollectionJobsIds={filteredDataCollectionJobsIds}
                                                          selectedDataCollectionJobId={selectedDataCollectionJobId}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="dataCollectionJobInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="dataCollectionJobInput"
                                onChange={searchDataCollectionJobHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <DataCollectionJobAccordion selectedDataCollectionJob={selectedDataCollectionJob}
                                        loadingSelectedDataCollectionJob={loadingSelectedDataCollectionJob}/>


            <div className="row systemIdentificationJobs">
                <div className="col-sm-6">
                    <h4 className="text-center inline-block emulationsHeader">
                        <SelectSystemIdentificationJobOrSpinner systemIdentificationJobsLoading={systemIdentificationJobsLoading}
                                                                systemIdentificationJobsIds={filteredSystemIdentificationJobsIds}
                                                                selectedSystemIdentificationJobId={selectedSystemIdentificationJobId}
                        />
                    </h4>
                </div>
                <div className="col-sm-4">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="systemIdentificationJobInput" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="systemIdentificationJobInput"
                                onChange={searchSystemIdentificationJobHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <SystemIdentificationJobAccordion selectedSystemIdentificationJob={selectedSystemIdentificationJob}
                                              loadingSelectedSystemIdentificationJob={loadingSelectedSystemIdentificationJob}/>

        </div>
    );
}

Jobs.propTypes = {};
Jobs.defaultProps = {};
export default Jobs;
