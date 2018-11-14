define([],function(){
	"use strict";
	return function CompressedGraph(graph){
		var _e_def,
			_n_def,
			_graphs_by_id,//hashtable of graph idx by graph id
			_graphs,
			//patterns,
			_current_graph,
			_date,
			_version;
		//initialize a new graph using the graph specified
		(function _init(g){
			if(g.version!="0.9") throw new Error("Wrong file version");
			_initObject(g);
			if(!g.graphs)return;
			_genGaphs(g.graphs);
			_compressGraphs();
		}(graph));
		/* log all the graph informations for debug purpose
		 */
		this.log = function log(){
			console.log("==========================");
			console.log(_current_graph,_date,_version);
			console.log("==========================");
			console.log("node att :");
			console.log(_n_def);
			console.log("==========================");
			console.log("edge att :");
			console.log(_e_def);
			console.log("==========================");
			for(let graphId=0;graphId<_graphs.length;graphId++){
				console.log(_graphs[graphId].id);
				console.log(_graphs[graphId]);
			}
		};
		/* create a new object Compressed graph.
		 * initialize all its default values,
		 * @input graph : the reference graph object for _version and _date 
		 */
		function _initObject(graph){
			_e_def = {/*all the edges attributes except source/target/id*/},
			_n_def = {coord:{}/* all the nodes attributes except id and hierarchy */},
			_graphs = [/* list of all graphs */],
			_graphs_by_id = {/* hashtable 'graph id' => 'index'*/},
			//patterns = 
			_current_graph =-1,//the current graph viewed
			_date = (graph && graph.date)?graph.date:_newDate("/"),
			_version = (graph && graph.version)?graph.version:"v_0."+_newDate("_",true);
		};
		/* generate a new _date string.
		 * @input sep : the separator character
		 * @input time : if true : add the current time to the _date
		 * @return : a string representing the _date
		 */
		function _newDate(sep,time){
			var d = new Date();
			return d.getDate()+sep+(d.getMonth()+1)+sep+d.getFullYear()+(time?sep+d.getTime():"");
		}
		/* add all the graphs of the network 
		 * @input graph_l : all the graphs objects.
		 */
		function _genGaphs(graph_l){
			console.log("generating graphs...");
			if(graph_l["_ALL"]){
				_initGraph("_ALL");
				_modCurrentGraph(_graphs.length-1);
				console.log("init all");
				_genGraph(graph_l["_ALL"]);
				delete graph_l["_ALL"];
			}
			var keys_l=Object.keys(graph_l);
			for(let i=keys_l.length-1;i>=0;i--){
				_initGraph(keys_l[i]);
				console.log("init "+keys_l[i]);
				_modCurrentGraph(_graphs.length-1);
				_genGraph(graph_l[keys_l[i]]);
			}
		};
		/* create a new graph object
		 * @input graph_id : the layout id
		 * this graph is added at the end of the graphs list, then it became the new _current_graph
		 */
		function _initGraph(graph_id){
			_graphs.push({
				id:graph_id,
				zoom:1,
				nodes_by_id:{},
				nodes_by_level:[],
				nodes_by_filters:{},
				root:{},
				leafs:{},
				edges_by_id:{},
				edges_by_filters:{},
				edges_by_source:{},
				edges_by_target:{},
				rw_rules:null,
				filters:null,
				n_count:0,
				e_count:0,
				default_layout:null,
				data_folder:null,
				bbox:null
			});
			_graphs_by_id[graph_id]=_graphs.length-1;
		}
		/* create a graph with masks for the specific graph entry of JSon file
		 * @input graph : a graph entry
		 * update the _current_graph !
		 */
		function _genGraph(graph){
			if(graph.rwRules){//add rw_rules to the graph
				_graphs[_current_graph].rw_rules = graph.rwRules;
				graph.rwRules=null;
			}
			if(graph.filters){
				_graphs[_current_graph].filters=graph.filters;
				//graph.filters=null;		
			} 			
			if(graph.zoom) _graphs[_current_graph].zoom=graph.zoom;//add zoom to the graph
			if(graph.filters){//add sorter object for each sorters defined.
				for(let k_i=graph.filters.length-1;k_i>=0;k_i--)
						_graphs[_current_graph].nodes_by_filters[graph.filters[k_i]]={};
			}if(graph.defaultLayout) _graphs[_current_graph].default_layout=graph.defaultLayout;
			if(graph.dataFolder) _graphs[_current_graph].data_folder=graph.dataFolder;
			if(graph.bbox) {
				//console.log(graph.bbox);
				_graphs[_current_graph].bbox={};
				let lyt = Object.keys(graph.bbox);
				for(let i=lyt.length-1;i>=0;i--)
					_graphs[_current_graph].bbox[lyt[i]]={x:graph.bbox[lyt[i]][0],y:graph.bbox[lyt[i]][1],width:graph.bbox[lyt[i]][2],height:graph.bbox[lyt[i]][3]};
				//console.log(_graphs[_current_graph].bbox);
			}
			if(graph.nodes){//add all the nodes.
				let nodes_keys = Object.keys(graph.nodes);
				for(let key_id=nodes_keys.length-1;key_id>=0;key_id--)
					_addNode(nodes_keys[key_id],graph.nodes[nodes_keys[key_id]]);
			}if(graph.edges){//add all the edges
				let edges_keys = Object.keys(graph.edges);
				for(let key_id=edges_keys.length-1;key_id>=0;key_id--)
					_addEdge(edges_keys[key_id],graph.edges[edges_keys[key_id]]);
			}
			//console.log(graph)
			_computeHierarchie();
		}
		/* add a new node to the graph
		 * compress this node in the _n_def
		 * @input n_id : the node id
		 * @input n : the node object
		 * this function is called on the current selected graph
		 */
		function _addNode(n_id,n){
			n_id = "_n_"+n_id;
			if(n.hierarchy){
				//if a hierarchy is defined : add it to the node and remove it from the graph file
				if(!n.hierarchy.parents) 
					throw new Error("hierarchy defined without parents for "+n_id);
				if(!Array.isArray(n.hierarchy.parents))
					n.hierarchy.parents=[n.hierarchy.parents];	
				n.hierarchy.parents=n.hierarchy.parents.map(e => "_n_"+e);
			}
			var node ={
				id:n_id,
				hierarchy:{//!!! parents is a list, others are associative lists.
					"parents":n.hierarchy?n.hierarchy.parents:null,
					"children":null,	
					"depth":null
				},coord:{/* all the node layout coords */}
			};
			if(n.coord){//if the node in the graph structure has a coord structure, inline it,
				let layout;
				if(_graphs[_current_graph].bbox){
					layout=Object.keys(_graphs[_current_graph].bbox);
					for(let i=layout.length-1;i>=0;i--)
						if(!n.coord[layout[i]] && (_current_graph==0 || !_graphs[0].nodes_by_id[n_id] || !_graphs[0].nodes_by_id[n_id].coord[layout[i]])) 
							_graphs[_current_graph].bbox[layout[i]]["sim"] = true;
				}
				if(_current_graph!=0 && _graphs[0].bbox ){
					layout = Object.keys(_graphs[0].bbox);
					for(let i=layout.length-1;i>=0;i--)
						if(!n.coord[layout[i]] && (!_graphs[0].nodes_by_id[n_id] || !_graphs[0].nodes_by_id[n_id].coord[layout[i]])) 
							_graphs[0].bbox[layout[i]]["sim"] = true;
				}
				_compressObj(n.coord,_n_def.coord,node.coord);
				//delete n.coord;
			}
			//add the node ref to all its filter lists.
			_addFilters(n,_graphs[_current_graph].nodes_by_filters,node);
			if(n.hierarchy) delete n.hierarchy;//remove hie and coord before compression.
			if(n.coord)delete n.coord;
			_compressObj(n,_n_def,node);
			_graphs[_current_graph].nodes_by_id[n_id]=node;
			_graphs[_current_graph].n_count++;
		}
		/* add filter functions for specific objects.
		 * filter are defined in a graph and are associated with object keys values.
		 * @input old_o : the json object.
		 * @input hash : the filter hashtable (node by value by filter)
		 * @input new_o : the object to refere in the hashtable.
		 */
		function _addFilters(old_o,hash,new_o){
			let filters=_graphs[_current_graph].filters;
			if(!filters) return;
			for(let k_i=filters.length-1;k_i>=0;k_i--){//filters : the list of filters
				let path = filters[k_i].split(".");
				if(path.length>1){
					//console.log("path",path);
					let tmp_obj = old_o,
						fp;
					for(fp = 0;fp<path.length-1;fp++){
						if(!tmp_obj[path[fp]]) break;
						tmp_obj=tmp_obj[path[fp]];
					}
					//console.log("val",fp,path.length,fp!=path.length-2,tmp_obj,path[path.length-1],!tmp_obj[path[path.length-1]]);
					if(fp!=path.length-1 || !tmp_obj[path[path.length-1]]) continue;
					if(!Array.isArray(tmp_obj[path[path.length-1]])) tmp_obj[path[path.length-1]]=[tmp_obj[path[path.length-1]]];
					//console.log("val2",tmp_obj[path[path.length-1]],typeof tmp_obj[path[path.length-1]][0],typeof tmp_obj[path[path.length-1]][0]!="string");
					if(typeof tmp_obj[path[path.length-1]][0]!="string") continue;
					//console.log("may be here ?");
					old_o[filters[k_i]]=tmp_obj[path[path.length-1]];
				}if(!old_o[filters[k_i]])continue;
				//add an array for the specific filter value
				if(!Array.isArray(old_o[filters[k_i]])) old_o[filters[k_i]]=[old_o[filters[k_i]]];
				//for each filter value in the node, add this node in the filter hashtable
				for(let i=old_o[filters[k_i]].length-1;i>=0;i--){	
					//add this value to the filter hash 
					if(!hash[filters[k_i]]) hash[filters[k_i]]={};
					//console.log(hash);
					if(!hash[filters[k_i]][old_o[filters[k_i]][i]])
						hash[filters[k_i]][old_o[filters[k_i]][i]]=[];
					hash[filters[k_i]][old_o[filters[k_i]][i]].push(new_o);			
				}	
			}
		}
		/* accessor function : get the bounding box of the current graph
		 * @input lyt : the layout to fit
		 * @return [x,y,w,h] : box of the graph for this layout or null if it doesn't exist
		 */
		this.getBBox = function getBBox(lyt){
			let g = _current_graph;
			if(_graphs[_current_graph].bbox && _graphs[_current_graph].bbox[lyt] )
				return _graphs[_current_graph].bbox[lyt];
			else if(_graphs[0].bbox && _graphs[0].bbox[lyt])
				return _graphs[0].bbox[lyt];
			else return null;
		}
		/* accessor function : get the defined data folder to check for images/css/spec for the current graph
		 * @ return : the current graph dataFolder (string)
		 */
		this.getDataFolder = function getDataFolder(){
			if(_graphs[_current_graph].data_folder) 
				return _graphs[_current_graph].data_folder;
			if(_graphs[0].data_folder)
				return _graphs[0].data_folder;
			else return null;
		}
		/* accessor function : get the defined default layout for the current graph
		 * @ return : the current graph default layout (string: layout name)
		 */
		this.getDefaultLayout = function getDefaultLayout(){
			if(_graphs[_current_graph].default_layout) 
				return _graphs[_current_graph].default_layout;
			if(_graphs[0].default_layout)
				return _graphs[0].default_layout;
			else return null;
		}
		/* compress multiples object to avoid attribute values redundencie.
		 * this function asume that a value is strictly bigger in size than a reference.
		 * all values are stocked without redundence in one object.
		 * each new object has only reference to the value position.
		 * @input obj : the object to compress.
		 * @input ref : the reference object where values are stored.
		 * @input new_obj : the compressed version of the object.
		 */
		function _compressObj(obj,ref,new_obj){
			var a_k = Object.keys(obj);
			//for each key in the node object : compress it into ref
			for(let k_i = a_k.length-1;k_i>=0;k_i--){
				//if this key doesn't exist add it to the ref
				if(!ref[a_k[k_i]])ref[a_k[k_i]]=[];
				//if key value !array, value ->[value]
				if(obj[a_k[k_i]] && !Array.isArray(obj[a_k[k_i]]))
					obj[a_k[k_i]]=[obj[a_k[k_i]]];
				//add each value to the ref and add a ref to it in the node of the graph
				for(let val_i = obj[a_k[k_i]].length-1;val_i>=0;val_i--){
					let value_idx = ref[a_k[k_i]].indexOf(obj[a_k[k_i]][val_i]);
					if(value_idx == -1){
						ref[a_k[k_i]].push(obj[a_k[k_i]][val_i]);
						value_idx=ref[a_k[k_i]].length-1;
					}	
					if(!new_obj[a_k[k_i]]) new_obj[a_k[k_i]]=[];
					new_obj[a_k[k_i]].push(value_idx);	
				}
			}
		}
		/* add a new edge to the graph.
		 * also add this edge to all the edges hashtable and layout dependant tables
		 * @input e_id : the edge id
		 * @input e : the new edge (welcom to!)
		 * this function is called on the current selected graph
		 */
		function _addEdge(e_id,e){
			e.src = "_n_"+e.src;
			e.tgt = "_n_"+e.tgt;
			var edge = {
					id:e_id,
				source:(_graphs[_current_graph].nodes_by_id[e.src]?
							_graphs[_current_graph].nodes_by_id[e.src]:
							_graphs[_graphs_by_id["_ALL"]].nodes_by_id[e.src]),
				target:(_graphs[_current_graph].nodes_by_id[e.tgt]?
						_graphs[_current_graph].nodes_by_id[e.tgt]:
						_graphs[_graphs_by_id["_ALL"]].nodes_by_id[e.tgt]),
				dir:e.dir
			};
			if(!edge.source) throw new Error("Undefined edge source "+e_id+" in "+_graphs[_current_graph].id);
			if(!edge.target) throw new Error("Undefined edge target "+e_id+" in "+_graphs[_current_graph].id);
			delete e.dir;
			delete e.src;
			delete e.tgt;
			_compressObj(e,_e_def,edge);
			_graphs[_current_graph].edges_by_id[e_id] = edge;
			if(!_graphs[_current_graph].edges_by_target[edge.target.id])
				_graphs[_current_graph].edges_by_target[edge.target.id]={};
			_graphs[_current_graph].edges_by_target[edge.target.id][e_id] = edge;
			if(!_graphs[_current_graph].edges_by_source[edge.source.id])
				_graphs[_current_graph].edges_by_source[edge.source.id]={};
			_graphs[_current_graph].edges_by_source[edge.source.id][e_id] = edge;
			_addFilters(e,_graphs[_current_graph].edges_by_filters,edge);
			_graphs[_current_graph].e_count++;
		}
		/* accessor function : add a new node
		 * @input abs : the node abstraction : [node id list]
		 * @input coord : the node coordinate : {[[layout name]]:[x,y(,z)]}
		 * @input attr: the node attributes : [["attribute key","attribute value] list]
		 * !!! no redundency check !!!
		 * this function is called on the current selected graph
		 */
		this.addNode = function addNode(abs,coord,attr){
			var new_node = {};
			if(abs)new_node.hierarchy={parents:abs};
			if(coord) new_node.coord=coord;
			if(attr){
				for(let i = attr.length-1;i>=0;i--)
					new_node[attr[i][0]]=attr[i][1];
			}
			var n_id = _genId("__n_");
			_addNode(n_id,new_node);
			_updateParenting(_graphs[_current_graph].nodes_by_id[n_id]);
			_depthCount(_graphs[_current_graph].nodes_by_id[n_id]);
			return n_id;
		};
		/* update parenting relation for a node n.
		 * @input n : the node to update
		 * this function gets a node with parents id and convert it to
		 * a node with a list of ref to its parents, a depth and children
		 * !!! this function doesn't update root and leafs !!!
		 */
		function _updateParenting(n){
			//console.log(n);
			if(!n.hierarchy || !n.hierarchy.parents) return;
			let nodes = _graphs[_current_graph].nodes_by_id;
			
			for(let i = n.hierarchy.parents.length-1;i>=0;i--){
				n.hierarchy.parents[i]=nodes[n.hierarchy.parents[i]];
				if(!n.hierarchy.parents[i].hierarchy.children)
					n.hierarchy.parents[i].hierarchy.children={};
				n.hierarchy.parents[i].hierarchy.children[n.id]=n;
			}
		}
		/* create a new id using a specified prefix
		 * @input pre : the id prefix
		 */
		function _genId(pre){
			return pre+(pre=="__n_"?_graphs[_current_graph].n_count:_graphs[_current_graph].e_count);
		}
		/* extend the hierarchy structure of each node based on the abstraction relation
		 * add children and depth attributes.
		 * this function is called on the current selected graph
		 */
		function _computeHierarchie(){
			let nodes = _graphs[_current_graph].nodes_by_id,
				n_k = Object.keys(nodes);
			for(let n_ix = n_k.length-1;n_ix>=0;n_ix--){
				//console.log(nodes[n_k[n_ix]]);
				if(!nodes[n_k[n_ix]].hierarchy.parents)
					_graphs[_current_graph].root[n_k[n_ix]]=nodes[n_k[n_ix]];
				else
					_updateParenting(nodes[n_k[n_ix]]);			
			}
			nodes = _graphs[_current_graph].root,
			n_k = Object.keys(nodes);
			for(let k_i=n_k.length-1;k_i>=0;k_i--)
				_depthCount(nodes[n_k[k_i]]);
		}
		/* calculate or recalculate the depth for each node of the subgraph with n as root
		 * @input n : a Dag root.
		 * Modify the whole DAG on place.
		 * This function is called on the current graph.
		 * this function update root and leafs structures
		 * !!!! Recursive function !!!!
		 */
		function _depthCount(n){
			if(!n.hierarchy.parents){
				n.hierarchy.depth=0;
				_graphs[_current_graph].root[n.id]=n;
			}else{
				if(_graphs[_current_graph].root[n.id])
					_graphs[_current_graph].root[n.id]=null;
				
				n.hierarchy.depth=n.hierarchy.parents.reduce(function(acc,e){
					if(e.id==n.id) throw Error("Node self loop ! : "+n.id);
					return Math.max(e.hierarchy.depth,acc)
				},0)+1;
			}
			if(!_graphs[_current_graph].nodes_by_level[n.hierarchy.depth])
				_graphs[_current_graph].nodes_by_level[n.hierarchy.depth]={};
			_graphs[_current_graph].nodes_by_level[n.hierarchy.depth][n.id]=n;
			if(_graphs[_current_graph].nodes_by_level[n.hierarchy.depth-1] && 
			_graphs[_current_graph].nodes_by_level[n.hierarchy.depth-1][n.id])
				_graphs[_current_graph].nodes_by_level[n.hierarchy.depth-1][n.id] = null;
			if(n.hierarchy.children){
				if(_graphs[_current_graph].leafs[n.id])
					_graphs[_current_graph].leafs[n.id]=null;
				let ch_k = Object.keys(n.hierarchy.children);
				for(let ch_ix = ch_k.length-1;ch_ix>=0;ch_ix--)
					_depthCount(n.hierarchy.children[ch_k[ch_ix]]);
			}else{
				_graphs[_current_graph].leafs[n.id]=n;
			}
		}
		/* change the currently selected graph to a new one 
		 * @input mod_idx : the graph index in the graphs table
		 */
		function _modCurrentGraph(mod_idx){
			_current_graph=mod_idx;
		}
		/* change the currently selected graph to a new one using id
		 * @input graph_id : the graph id.
		 */
		this.chGraph = function chGraph(graph_id){
			_modCurrentGraph(_graphs_by_id[graph_id]);
		}
		/* accessor function : add a new edge
		 * @input src: the source node id
		 * @input tgt : the tgt node id
		 * @input dir : the dir of the edge : boolean
		 * @input attr: the edge attributes : [["attribute key","attribute value] list]
		 * !!! no redundency check !!!
		 * this function is called on the current selected graph
		 */
		this.addEdge = function addEdge(src,tgt,dir,att){
			let e_id = _genId("__e_"),
				edge ={ src:src , tgt:tgt };
			if(dir)
				edge.dir=true;
			if(att){
				for(let i = attr.length-1;i>=0;i--)
					edge[attr[i][0]]=attr[i][1];
			}
			_addEdge(e_id,edge);
			return e_id;
		}
		/* Exact copy of a node.
		 * this function return a new node equivalent to the n node. this node need to be used via _addNode();
		 * this node also need to have a new id if it has to be added to a graph.
		 * @input n : the node to copy
		 * @return new_n : a clone of n.
		 * !!! this clone has no references to other nodes but only ids. 
		 * !!! this clone is the minimale structure embeding all the information for a specific node.
		 */
		function _nodeCopy(n){//Work in progress !!!!
			var new_n={id:n.id};
			if(n.coord)
				new_n.coord=_copyAssos(n.coord);
			if(n.hierarchy){
				new_n.hierarchy={};
				if(n.hierarchy.parents)
					new_n.hierarchy.abstraction=Object.keys(n.hierarchy.parents);
			}
			let n_k = Object.keys(n);
			for(let k_i = n_k.length-1;k_i>=0;k_i--){
				if(n_k[k_i]!=coord && n_k[k_i]!=hierarchy)
					new_n[n_k[k_i]]=n[n_k[k_i]];
			}
				
			return new_n;
		}
		/* copy an associative table.
		 * @input tbl : the table to copy
		 * @return : a new associative table. this new table is an exact copy of tbl.
		 * carefull : this table may contain reference to other nodes.
		 */
		function _copyAssos(tbl){
			var new_tbl ={};
			let k_id = Object.keys(tbl);
			for(let ix = k_id.length-1;ix>=0;ix--)
				new_tbl[k_id[ix]]=tbl[k_id[ix]].concat();
			return new_tbl;
		}
		/* accessor function : return the list of all nodes of a graph.
		 * @input f_l : the list of filters to use for those nodes.
		 * @return : an id list.
		 */
		this.getNodes = function getNodes(f_l){
			let ret = {};
			if(!f_l){
				if(_current_graph==0)return Object.keys(_graphs[_current_graph].nodes_by_id);
				return Object.keys(_graphs[_current_graph].nodes_by_id).concat(Object.keys(_graphs[0].nodes_by_id));
			}else{
				for(let i=f_l.length-1;i>=0;i--){
					let flt = _graphs[_current_graph].nodes_by_filters[f_l[i]];
					if(flt){
						let n_id_l = Object.keys(flt);
						for(let j=n_id_l.length-1;j>=0;j--){
							ret[n_id_l[j]]=n_id_l[j];
						}
					}flt = _graphs[0].nodes_by_filters[f_l[i]];
					if(flt){
						let n_id_l = Object.keys(flt);
						for(let j=n_id_l.length-1;j>=0;j--){
							ret[n_id_l[j]]=n_id_l[j];
						}
					}
				}
			}
			
			
			return Object.keys(ret);
		}
		/* accessor function : check if a specific node exist in the current graph or in the default one
		 * @return : true if it exist, false if not
		 */
		this.nodeExist = function nodeExist(n_id){
			return _graphs[_current_graph].nodes_by_id[n_id] || _graphs[0].nodes_by_id[n_id];
		}
		/* accessor function : check if a specific edge exist in the current graph or in the default one
		 * @return : true if it exist, false if not
		 */
		this.edgeExist = function edgeExist(e_id){
			return _graphs[_current_graph].edges_by_id[e_id] || _graphs[0].edges_by_id[e_id];
		}
		/* accessor function : return the list of all edges of the current graph
		 * @input f_l : the list of filters to use for those edges.
		 * @return : an id list
		 */
		this.getEdges = function getEdges(f_l){
			if(!f_l)f_l = _graphs[_current_graph].filters;
			let ret = {};
			for(let i=f_l.length-1;i>=0;i--){
				let flt = _graphs[_current_graph].edges_by_filters[f_l[i]];
				if(flt){
					let n_id_l = Object.keys(flt);
					for(let j=n_id_l.length-1;j>=0;j--){
						ret[n_id_l[j]]=n_id_l[j];
					}
				}flt = _graphs[0].edges_by_filters[f_l[i]];
				if(flt){
					let n_id_l = Object.keys(flt);
					for(let j=n_id_l.length-1;j>=0;j--){
						ret[n_id_l[j]]=n_id_l[j];
					}
				}
			}
			return Object.keys(ret);
		};
		/* accessor function : return the list of all filters for the current graph
		 * @return : a list of filters key name
		 */
		this.getFilters = function getFilters(){
			if(_graphs[_current_graph].filters && _graphs[_current_graph].filters.length>0)
				return _graphs[_current_graph].filters;
			else return _graphs[0].filters;
		}
		/* accessor function : return the date of the model
		 * @return : a date
		 */
		this.getDate = function getDate(){
			return date;
		};
		/* accessor function : return the version of the model
		 * @return : a string corresponding to the version
		 */
		this.getVersion = function getVersion(){
			return version;
		};
		/* accessor function : return the current graph id
		 * @return : graph id
		 */
		this.getCurrentGraph = function getCurrentGraph(){
			return _graphs[_current_graph].id;
		};
		/* accessor function : return all the existing graphs id
		 * @return : graph id list
		 */
		this.getGraphs = function getGraphs(){
			return Object.keys(_graphs_by_id);
		};
		/* accessor function : return the base zoom of the current graph
		 * @return : zoom : float
		 */
		this.getZoom = function getZoom(){
			return _graphs[_current_graph].zoom;
		};
		/* accessor function : return levels information about the current graph
		 * @input lvl : if defined : return all the node of this level, else, return the depth of the graph
		 * @return : a node id list or an int
		 *  warning : this function doesn't merge _ALL and the current graph !
		 */
		this.getNLevel = getNLevel;
		function getNLevel(lvl){
			if(!lvl) return _graphs[_current_graph].nodes_by_level.length;
			return Object.keys(_graphs[_current_graph].nodes_by_level[lvl]);
		};
		/* accessor function : return all children of a specific node in the current graph
		 * @input n_id : the node id
		 * @return : node id list
		 */
		this.getChildren = function getChildren(n_id){
			let gr = _current_graph;
			if(!_graphs[_current_graph].nodes_by_id[n_id]) gr = 0;
			if(!_graphs[gr].nodes_by_id[n_id].hierarchy.children) return null;
			return Object.keys(_graphs[gr].nodes_by_id[n_id].hierarchy.children);
		};
		/* accessor function : return all parents of a specific node in the current graph
		 * @input n_id : the node id
		 * @return : node id list
		 */
		this.getParents = function getParents(n_id){
			return _graphs[_current_graph].nodes_by_id[n_id].hierarchy.parents.map(e => e.id);
		};
		this.getDepth = function getDepth(n_id){
			let gr = _current_graph;
			if(!_graphs[gr].nodes_by_id[n_id].hierarchy)gr = 0;
			if(!_graphs[gr].nodes_by_id[n_id].hierarchy) return 1;
			return _graphs[gr].nodes_by_id[n_id].hierarchy.depth;
		}
		/* accessor function : return all roots in the current graph
		 * @return : node id list
		 */
		this.getRoots = function getRoots(){
			return Object.keys(_graphs[_current_graph].root);
		};
		/* accessor function : return all leafs in the current graph
		 * @return : node id list
		 */
		this.getLeafs = function getLeafs(){
			return Object.keys(_graphs[_current_graph].nodes_by_id[n_id].leafs);
		};
		/* accessor function : return all the edges with a specific node source in current graph
		 * @input n_id : the source node id
		 * @return : edge id list
		 */
		this.getEBySource = function getEBySource(n_id){
			let gr = _current_graph;
			if(!_graphs[gr].edges_by_source[n_id]) gr =0
			if(_graphs[gr].edges_by_source[n_id])
				return Object.keys(_graphs[gr].edges_by_source[n_id]);
			else return [];
		};
		/* accessor function : return all the edges with a specific node target in current graph
		 * @input n_id : the target node id
		 * @return : edge id list
		 */
		this.getEByTarget = function getEByTarget(n_id){
			let gr = _current_graph;
			if(!_graphs[gr].edges_by_target[n_id]) gr =0;
			if(_graphs[gr].edges_by_target[n_id])
				return Object.keys(_graphs[gr].edges_by_target[n_id]);
			else return [];
		};
		/* accessor function : return all the attributes of a specific node in current graph
		 * @input n_id : the node id
		 * @input att_k : the attribute key to search (if undefined return all existing keys)
		 * @return : att val list or att key list
		 */
		this.getNAtt = function getNAtt(n_id,att_k){
			let gr = _current_graph;
			if(gr == 0) return _getNAtt(0,n_id,att_k).concat();
			return _getNAtt(gr,n_id,att_k).concat(_getNAtt(0,n_id,att_k));
			
		};
		function _getNAtt(g_id,n_id,att_k){
			let node = _graphs[g_id].nodes_by_id[n_id];
			if(!node) return [];
			if(!att_k){
				let att = Object.keys(node);
				for(let i = att.length-1;i>=0;i--){
					if(att[i]=="coord" || att[i] == "hierarchy" || att[i] == "id")
						att.splice(i,1);
				}
				return att;
			} else if(node[att_k])
				return node[att_k].map(e => _n_def[att_k][e]);
			else return [];
		}
		/* accessor function : return all the attributes of a specific edge in current graph
		 * @input e_id : the edge id
		 * @input att_k : the attribute key to search (if undefined return all existing keys)
		 * @return : att val list or att key list
		 */
		this.getEAtt = function getEAtt(e_id,att_k){
			let gr = _current_graph;
			if(gr == 0) return _getEAtt(0,e_id,att_k).concat();
			return _getEAtt(gr,e_id,att_k).concat(_getEAtt(0,e_id,att_k));
		}
		function _getEAtt(g_id,e_id,att_k){
			let gr = _current_graph;
			let edge = _graphs[gr].edges_by_id[e_id];
			if(!edge) return [];
			if(!att_k){
				let att = Object.keys(edge);
				for(let i = att.length-1;i>=0;i--){
					if(att[i]=="source" || att[i] == "target" || att[i] == "id" || att[i]!="dir")
						att.splice(i,1);
				}
				return att;
			} else if(edge[att_k])
				return edge[att_k].map(e => _e_def[att_k][e]);
			else return [];
		};
		/* accessor function : return all the node attributes values for a specific key in the current graph
		 * @input att_k : the attribute key to search
		 * @return : att val list
		 */
		this.getNAttValList = function getNAttValList(att_k){
			if(!_n_def[att_k]) return [];
			return _n_def[att_k].concat();
		};
		
		this.getNFlValList = function getNFlValList(att_k){
			let g = _current_graph;
			if(!_graphs[g].nodes_by_filters[att_k]) g = 0;
			if(!_graphs[g].nodes_by_filters[att_k]) return null;
			else return 
		}
		/* accessor function : return all the edge attributes values for a specific key in the current graph
		 * @input att_k : the attribute key to search
		 * @return : att val list
		 */
		this.getEAttValList = function getEAttValList(att_k){
			if(!_e_def[att_k]) return [];
			if(getNLevel()>1) return _e_def[att_k].concat(["hierarchy"]);
			return _e_def[att_k].concat();
		};
		/* accessor function : return all the node coordinates in the current graph
		 * @input layout : the layout to check
		 * @return : coord list
		 */
		this.getCoordList = function getCoordList(layout){
			if(!layout) return Object.keys(_n_def.coord);
			if(_n_def.coord[layout])
				return _n_def.coord[layout].concat();
			else return null;
		};
		/* acessor function : get the whole layout list
		 * @return : a list of string (layout name)
		 * warning : some layout may not exist for the current graph.
		 */
		this.getLayout = function getLayout(){
			return Object.keys(_n_def.coord);
		}
		/* accessor function : return a node coordinate / layout in the current graph
		 * @input n_id : the node id
		 * @input layout : the layout to check, if not defined, return the layout list of this node
		 * @return : coord list / layout list
		 */
		this.getCoord = function getCoord(n_id,layout){
			let gr = _current_graph;
			if(gr == 0) return _getCoord(0,n_id,layout).concat();
			return _getCoord(gr,n_id,layout).concat(_getCoord(0,n_id,layout));
		}
		function _getCoord(g_ix,n_id,layout){
			let gr = g_ix;
			if(!_graphs[gr].nodes_by_id[n_id] || !_graphs[gr].nodes_by_id[n_id].coord[layout]) return [];
			if(!layout) return Object.keys(_graphs[gr].nodes_by_id[n_id].coord);
			return _graphs[gr].nodes_by_id[n_id].coord[layout].map(e => _n_def.coord[layout][e]);
		};
		/* accessor function : return an edge source in the current graph
		 * @input e_id : the edge id
		 * @return : a node id
		 */
		this.getSource = function getSource(e_id){
			if(_graphs[_current_graph].edges_by_id[e_id])
				return _graphs[_current_graph].edges_by_id[e_id].source.id;
			else return _graphs[0].edges_by_id[e_id].source.id;
		};
		/* accessor function : return an edge target in the current graph
		 * @input e_id : the edge id
		 * @return : a node id
		 */
		this.getTarget = function getTarget(e_id){
			if(_graphs[_current_graph].edges_by_id[e_id])
				return _graphs[_current_graph].edges_by_id[e_id].target.id;
			else return _graphs[0].edges_by_id[e_id].target.id;
		};
		/* accessor function : return an edge orientation in the current graph
		 * @input e_id : the edge id
		 * @return : bool : true if oriented (source->target) false if none oriented
		 */
		this.getDir = function getDir(e_id){
			if(_graphs[_current_graph].edges_by_id[e_id])
				return _graphs[_current_graph].edges_by_id[e_id].dir;
			else return _graphs[0].edges_by_id[e_id].dir;
		}
		/* accessor function : add a new graph to the model.
		 * @input g_id : the new graph id.
		 * @return : the new graph id.
		 */
		this.addGraph = function addGraph(g_id){
			if(_graphs.length==0){
				_initGraph("_ALL");
			}
			_initGraph(g_id);
			_modCurrentGraph(_graphs.length-1);
			return g_id;
		}
		/* accessor function : return a minified version of the graph
		 * this function return all the nodes and edges of the current graph union those of _ALL
		 * this function dodge multiple calls to sub function.
		 * @return {nodes,edges} a graph structure with hierarchy between nodes.
		 */
		this.getMiniGraph = function getMiniGraph(){
			console.log("Generating view...");
			let n_ret ={},
				e_ret ={},
				h_ret = {},
				leafs=[],
				all_leafs=[];
			if(_graphs[_current_graph].leafs)//get the current graph leafs
				leafs = Object.keys(_graphs[_current_graph].leafs);
			if(_current_graph!=0 && _graphs[0].leafs)//get _ALL leafs
				all_leafs = Object.keys(_graphs[0].leafs);
			for(let i=all_leafs.length-1;i>=0;i--)//get the whole _ALL graph minified node hierarchy
				_genDagList(all_leafs[i],n_ret,h_ret);
			for(let i=leafs.length-1;i>=0;i--)//get the whole current graph minified node hierarchy
				_genDagList(leafs[i],n_ret,h_ret);
			let n_list = Object.keys(n_ret);
			//console.log(n_ret);
			for(let i = n_list.length-1;i>=0;i--){//for each node add edges to the list (hierarchycal edges are not added)
				let node_orr = -1;//unknown origine : 0 : from current, 1: from _all, 2: from both
				if(_graphs[0].nodes_by_id[n_list[i]]) node_orr = 1;//this node is from the _ALL graph
				if(_graphs[_current_graph].nodes_by_id[n_list[i]]) node_orr++;//this node is from the current graph
				let e_candidates = [];//list of candidate edges
				if((node_orr==0 || node_orr==2) && _graphs[_current_graph].edges_by_source[n_list[i]])//check for edges in current graph if the node is from it
					e_candidates.push(_graphs[_current_graph].edges_by_source[n_list[i]]);
				if(node_orr>0 && _graphs[0].edges_by_source[n_list[i]])//check for edges in _ALL graph if the node is from it
					e_candidates.push(_graphs[0].edges_by_source[n_list[i]]);
				//console.log(e_candidates);
				for(let j = e_candidates.length-1;j>=0;j--){//get only source and target for each in n_ret
					let values = Object.values(e_candidates[j]).forEach(function(e){//only add the node to e_ret if its target is also in the minified graph
						if(n_ret[e.target.id])
							e_ret[e.id]={id:e.id,source:n_ret[e.source.id],target:n_ret[e.target.id]};
					});
					
				}
			}
			console.log("done");
			return{
				nodes:Object.values(n_ret),
				hie:Object.values(h_ret),
				edges:Object.values(e_ret)
			};
			
		}
		/* convert a whole dag into a minified dag list.
		 * terminal recursive function for Tree and Dag
		 * @input n_id : the node id
		 * @input n_ret : the list to update
		 */
		function _genDagList(n_id,n_ret,h_ret){
			if(!n_ret[n_id])
				n_ret[n_id]={id:n_id};
			let gr = _current_graph;
			if(!_graphs[_current_graph].nodes_by_id[n_id])gr =0;
			if(_graphs[gr].nodes_by_id[n_id].hierarchy.children){
				let ch_id = Object.keys(_graphs[gr].nodes_by_id[n_id].hierarchy.children);	
				if(!n_ret[n_id].children)
					n_ret[n_id].children = [];
				ch_id.forEach(function(p){
					if(n_ret[p] && n_ret[n_id].children.map(c => c.id).indexOf(p)==-1){
					n_ret[n_id].children.push(n_ret[p]);
					h_ret["__e"+p+"_"+n_id]={id:"__e"+p.id+"_"+n_id,source:n_ret[p],target:n_ret[n_id]};
					}
				})
			}
			if(_graphs[gr].nodes_by_id[n_id].hierarchy.parents){
				_graphs[gr].nodes_by_id[n_id].hierarchy.parents.forEach(function(p){
					_genDagList(p.id,n_ret,h_ret);	
				});
			}
		}
		/* accessor function : change the current coordinate of a node in a aspecific layout
		 * @input n_id : the node coordinate.
		 * @input layout : the layout to modify
		 * @coord : the coordinate set.
		 * !!! the function replace the current coordinate !!!
		 */
		this.setCoord = function setCoord(n_id,layout,coord){
			let old_c = null;
			if(_graphs[gr].nodes_by_id[n_id].coord[layout])
				old_c = _graphs[gr].nodes_by_id[n_id].coord[layout];
			_graphs[gr].nodes_by_id[n_id].coord[layout]=coord;
			return old_c			
		}
		/* compress the whole model using LeZi algorithm
		 * this function check for redundent pattern in all graph and nodes and replace it with a hierarchical pattern object.
		 */
		function _compressGraphs(){
			console.log("compressing...");
			console.log("HA...HA");
			//algorithme de compression par redondance double.
			//tout element trouvé deux fois (pattern ou element concret) devient un nouveau pattern.
			//use active LeZI algorithm for compression
		}
		
		
		
		
		
		
	 }
 });