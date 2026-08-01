cmake_minimum_required(VERSION 3.16)
project(gui_app LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 找 Qt6
find_package(Qt6 REQUIRED COMPONENTS Widgets)

add_executable(gui_app main.cpp)
add_executable(minecode minecode.cpp)

# 链接 Qt6
target_link_libraries(gui_app Qt6::Widgets)
target_link_libraries(minecode Qt6::Widgets)
