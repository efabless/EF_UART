## Run cocotb UVM Testbench:
In IP directory run:
 ```shell
 cd verify/uvm-python/
 ```
 ##### To run testbench for design with certain bus type 
 To run all tests:
 ```shell
 make run_all_tests BUS_TYPE=<bus_type>
 ```
 To run a certain test:
 ```shell
 make run_<test_name> BUS_TYPE=<bus_type>
 ```
 To run all tests with a tag: 
 ```shell
 make run_all_tests TAG=<new_tag> BUS_TYPE=<bus_type>
 ```
