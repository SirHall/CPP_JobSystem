#ifndef WorkPool_hpp
#define WorkPool_hpp

#include <boost/asio/io_service.hpp>
#include <boost/bind.hpp>
#include <boost/thread/thread.hpp>
#include <vector>

#include <stdint.h>
#include <functional>

class WorkPool{
    private:
        boost::asio::io_service ioService;
        boost::thread_group threadPool;
    public:
        WorkPool(unsigned int threadCount){
            boost::asio::io_service::work work(ioService);
            for(unsigned int i = 0; i < threadCount; i++)
                threadPool.create_thread(
                    boost::bind(&boost::asio::io_service::run, &ioService)
                );
        }
        ~WorkPool() = default;

        void Start(){
            if(ioService.stopped())
                ioService.run();
        }

        void Stop(){
            if(!ioService.stopped())
                ioService.stop();
        }

        template <class RetT, class ArgT, class F>
        void Submit(RetT (*func)(ArgT)){
            ioService.post(boost::bind(func));
        }
};

#endif